import base64
import hmac
import hashlib
import urllib

#encryption alg for amazon signature
def sig_maker(key, outer_dict, method):
	
	in_crypt = '{0}\n'.format(method)
	data_dict = outer_dict.copy()
	data_dict['target_url'] = data_dict['target_url'][data_dict['target_url'].find('//')+2:]
	in_crypt +=data_dict['target_url'].lower()[:data_dict['target_url'].find('.com')+4] +'\n'
	in_crypt += data_dict['target_url'].lower()[data_dict['target_url'].find('.com')+4:] +'\n'
	all_hidden = data_dict.items()
	all_hidden.remove(('target_url',data_dict['target_url']))
	all_hidden.sort(key=lambda x:str(x[0]))
	first = True	
	for item in all_hidden:
		in_crypt += urllib.urlencode(all_hidden)
	return base64.encodestring(hmac.new(key, in_crypt, hashlib.sha256).digest()).strip()
