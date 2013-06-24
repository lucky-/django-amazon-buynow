from amazon_buttons import buttonconf
from amazon_buttons import urls
from django.conf import settings
import base64
import hmac
import hashlib
from django.utils.safestring import mark_safe
import urllib
from django.core.urlresolvers import reverse


#encryption alg for button signature. for POST only
def sig_maker(key, outer_dict):
	
	in_crypt = 'POST\n'
	data_dict = outer_dict.copy()
	data_dict['target_url'] = data_dict['target_url'][data_dict['target_url'].find('//')+2:]
	in_crypt +=data_dict['target_url'].lower()[:data_dict['target_url'].find('.com')+4] +'\n'
	in_crypt += data_dict['target_url'].lower()[data_dict['target_url'].find('.com')+4:] +'\n'
	all_hidden = data_dict.items()
	all_hidden.remove(('target_url',data_dict['target_url']))
	all_hidden.sort(key=lambda x:str(x[0]))
	first = True	
	for item in all_hidden:
		if first:
			in_crypt += urllib.quote(item[0]).replace('/','%2F') + '=' + urllib.quote(item[1]).replace('/','%2F')
			first = False
		else:
			in_crypt += '&' + urllib.quote(item[0]).replace('/','%2F') + '=' + urllib.quote(item[1]).replace('/','%2F')
	return base64.encodestring(hmac.new(key, in_crypt, hashlib.sha256).digest()).strip()




class button:
	def __init__(self, b_data):
		self.b_data = b_data
	
		
	def render(self, sandbox = False,  signed=False, button_url = buttonconf.BUTTONURL):
		if signed:		
			prepd_data = buttonconf.DEFAULT_CRYPT_DATA
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
			prepd_data['signature'] = sig_maker(s_key, prepd_data)
		form ='<form action="{0}" method="post">'.format(prepd_data['target_url'])
		del prepd_data['target_url']
		for name, val in prepd_data.iteritems():
			form += '<input name="{0}" type="hidden" value="{1}" />'.format(name,val)
		form += '<input type="image" src="{0}" border="0" /></form>'.format(button_url)
		return mark_safe(form)		

	
