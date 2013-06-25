from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from amazon_buttons import models
import datetime
from django.conf import settings
import urllib
import urllib2
from amazon_buttons import buttonconf
from amazon_buttons import _crypt





@csrf_exempt
def ipn_handler(request):
	ipn = models.ipn_response()
	ipn.datetime = datetime.datetime.fromtimestamp(int(request.POST['transactionDate']))
	for key, val in request.POST.iteritems():
		attrib = getattr(ipn, key, None)
		if attrib:
			setattr(ipn, key, val)
	if settings.AMAZON_IPN_VERIFY:
		if settings.AMAZON_SANDBOX:
			ver_url = buttonconf.SANDBOX_VERIFY		
		else:
			ver_url = buttonconf.LIVE_VERIFY
		prepd_data = buttonconf.DEFAULT_DATA
		prepd_data['Action'] = 'VerifySignature'
		prepd_data['UrlEndPoint'] = ver_url
		prepd_data['HttpParameters'] = urllib.urlencode(request.POST)
		fin_url = urllib.urlencode(prepd_data)
		print fin_url
		
		
	else:
		ipn.save()
	return HttpResponse('Done')
	
