from amazon_buttons import buttonconf
from amazon_buttons import urls
from django.conf import settings

from django.utils.safestring import mark_safe
import urllib
from django.core.urlresolvers import reverse
from amazon_buttons import _crypt






class button:
	def __init__(self, b_data):
		self.b_data = b_data
	
		
	def render(self, sandbox = settings.AMAZON_SANDBOX,  signed=False, button_url = buttonconf.BUTTONURL):
		if signed:		
			prepd_data = buttonconf.DEFAULT_CRYPT_DATA
			prepd_data['accessKey'] = settings.AMAZON_ACCESS_KEY
		else:
			prepd_data = buttonconf.DEFAULT_DATA
		if settings.AMAZON_IPN:
			prepd_data['ipnUrl'] = settings.DOMAIN_FOR_AMAZON_IPN + reverse('amazon_ipn')
		for key, val in self.b_data.iteritems():
			prepd_data[key] = str(val)
		if sandbox:
			prepd_data['target_url'] = buttonconf.AMAZON_SANDBOX_URL
		else:
			prepd_data['target_url'] = buttonconf.AMAZON_URL
		if signed:
			s_key = settings.AMAZON_SECRET_KEY
			prepd_data['signature'] = _crypt.sig_maker(s_key, prepd_data,'POST')
		form ='<form action="{0}" method="post">'.format(prepd_data['target_url'])
		del prepd_data['target_url']
		for name, val in prepd_data.iteritems():
			form += '<input name="{0}" type="hidden" value="{1}" />'.format(name,val)
		form += '<input type="image" src="{0}" border="0" /></form>'.format(button_url)
		if signed:
			del prepd_data['signature']
		return mark_safe(form)		

	
