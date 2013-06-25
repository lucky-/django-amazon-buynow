from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from amazon_buttons import models
import datetime
from django.conf import settings






@csrf_exempt
def ipn_handler(request):
	ipn = models.ipn_response()
	ipn.datetime = datetime.datetime.fromtimestamp(int(request.POST['transactionDate']))
	for key, val in request.POST.iteritems():
		attrib = getattr(ipn, key, None)
		if attrib:
			setattr(ipn, key, value)
	if settings.AMAZON_IPN_VERIFY:
		pass
	else:
		ipn.save()
	return HttpResponse('Done')
	
