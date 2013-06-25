from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from amazon_buttons import models
import datetime
from django.conf import settings
import urllib
import urllib2
from amazon_buttons import buttonconf






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
		params = request.POST.copy()
		pre_params = dict(Action = 'VerifySignature', UrlEndPoint = settings.DOMAIN_FOR_AMAZON_IPN + request.path)
		ver_url += '?' + urllib.urlencode(pre_params) + '&' + urllib.urlencode(params)
		# for testing
		print ver_url
		req = urllib2.Request(ver_url)
		resp = urllib2.urlopen(req)
		print resp.read()
		
	else:
		ipn.save()
	return HttpResponse('Done')
	
