from amazon_buttons import buttonconf
from django.conf import settings
import base64
import hmac
import sha


#  Creates the different buttons. Default data for the buttons comes from buttonconf.py.  Standard data for all buttons can be entered in gen_data dict or individual data for each payment service can be entered in paypal_data,google_data,and amazon_data.  If both, the individual dictionaries will override.


class button_data:
	def __init__(self, b_data):
		self.b_data = b_data
	
		
	def render(self, sandbox = '', button_url = buttonconf.BUTTONURL):
		prepd_data = buttonconf.DEFAULT_DATA
		for key, val in self.b_data.iteritems():
			prepd_data[key] = str(val)
		#create signature
		s_key = settings.AMAZON_SECRET_KEY
		all_hidden = prepd_data.items()
		all_hidden.sort(key=lambda x:str(x[0]).lower())
		in_crypt = ''
		for item in all_hidden:
			in_crypt += (str(item[0]) + str(item[1]))
		prepd_data['signature'] = base64.encodestring(hmac.new(s_key, in_crypt, sha).digest()).strip()
		if sandbox:
			target_url = buttonconf.AMAZON_SANDBOX_URL + sandbox
		else:
			target_url = buttonconf.AMAZON_URL
		form ='<form action="{0}" method="post">'.format(target_url)
		for name, val in prepd_data.iteritems():
			form += '<input name="{0}" type="hidden" value="{1}" />'.format(name,val)
		form += '<input type="image" src="{0}" border="0" /></form>'.format(button_url)
		return form		

	
