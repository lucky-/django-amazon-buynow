from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from amazon_buttons import models
import datetime
from django.conf import settings
import urllib
from amazon_buttons import buttonconf
from amazon_buttons import _crypt
from django.core.urlresolvers import reverse
from xml.dom import minidom




@csrf_exempt
def ipn_handler(request):
	ipn = models.ipn_response()
	ipn.datetime = datetime.datetime.fromtimestamp(int(request.POST['transactionDate']))
	for key, val in request.POST.iteritems():
		attrib = getattr(ipn, key, None)
		if attrib:
			setattr(ipn, key, val)
	if settings.AMAZON_IPN_VERIFY:
		flagged = True
		if settings.AMAZON_SANDBOX:
			ver_url = buttonconf.SANDBOX_VERIFY		
		else:
			ver_url = buttonconf.LIVE_VERIFY
		prepd_data = buttonconf.DEFAULT_IPNVER_DATA
		prepd_data['UrlEndPoint'] = settings.DOMAIN_FOR_AMAZON_IPN + reverse('amazon_ipn')
		prepd_data['target_url'] = ver_url
		prepd_data['HttpParameters'] = urllib.urlencode(request.POST)
		prepd_data['AWSAccessKeyId'] = settings.AMAZON_ACCESS_KEY 
		prepd_data['Timestamp'] = datetime.datetime.now().isoformat()
		s_key = settings.AMAZON_SECRET_KEY
		prepd_data['Signature'] = _crypt.sig_maker(s_key, prepd_data,'GET')
		del prepd_data['target_url']
		ver_url += '?' + urllib.urlencode(prepd_data)
		resp = urllib.urlopen(ver_url)
		ver_node = minidom.parse(resp).getElementsByTagName('VerificationStatus')
		if ver_node:
			if str(ver_node[0].firstChild.data) == 'Success':
				flagged = False
		if flagged:
			ipn.ver_status = 'FLAG'
		else:
			ipn.ver_status =  'verified'
		ipn.save()
			
		
		
		
	else:
		ipn.save()
	return HttpResponse('Done')
	
