django-amazon-buynow
====================

Quick and easy dynamic amazon payments.




This app allows users to creat buttons for amazon simple payment dynamically on a website.



Installation:

1)Download the app and put amazon_buttons in your installed apps
2)put the following fields in settings:

Mandatory:

AMAZON_IPN
-boolean field. Choose whether or not amazon should send an asynchronos post request (webhook) to you notifying you of payment
AMAZON_SANDBOX
-boolean field. If true, requests will be sent to the amazon payment testing sandbox, which does not deal in real money.  If false, you will use their real service.

Optional:
(if signed buttons)
AMAZON_SECRET_KEY 
AMAZON_ACCESS_KEY 
-These are values used in creating signautres for your button.  If you want to sign your buttons (discussed later) you will need to enter these values.
(if ipn is on)
AMAZON_IPN_VERIFY
-Boolean field asking whether or not you want to verify that the ipn is really coming from amazon.  Requires that you are able to send outbound http requests. Also requires that your buttons are signed
DOMAIN_FOR_AMAZON_IPN
-this is your domain name where you want the ipn notification sent. No trailing slash. ex(http://www.example.com)

Additionally, if IPN is on, you need to add the following to your urls.
url(r'^ipn_handler/', include('amazon_buttons.urls')),



Usage:

1)In the view where you want to create the button, import amazon_buttons.buttonforms
2)Create an instance of the buttonforms.button instance and pass it a dictionary of the arguments you want included in the button.  A list of possible arguments can be found here:   (please note, if you are using signaures, you do not need to add the 'accessKey' argument as it will be taken from settings.AMAZON_ACCESS_KEY)
3)create the html form using the button object's .render() method.  This menthod should be passed a single boolean keyword argument 'signed'.  If true, this will create a signature and add it to the form. Keep in mind that you need to enable signatures in your seller settings on amazon for this to have any effect.


Example:
	In views.py

	from amazon_buttons import buttonforms
	from django.shortcuts import render_to_response
	from django.template import RequestContext

	def buy_something(request):
		button_dict = dict( amount='103.00', description='some item you want to buy', abandonURL='http://example.com/fail/', referenceId='123abc', returnUrl='http://example.com/success/') 
		form = buttonforms.button(button_dict).render(signed=True)
		return render_to_response('example.html', dict(form=form), context_instance=RequestContext(request))

	In settings.py
	
	AMAZON_SECRET_KEY  = 'ahjdkl1975rMRIy1m0jaklw3jlkfjiosjdfa'
	AMAZON_ACCESS_KEY = 'JSOkaspjg1827jakJFklqu'	
	AMAZON_SANDBOX = False
	AMAZON_IPN = False



	

IPN's:

If in AMAZON_IPN is set to True in settings, you need to add the following to your configuration:
In settings add:
AMAZON_IPN_VERIFY (Boolean)
DOMAIN_FOR_AMAZON_IPN (string without trailins slash.  This is ONLY your top level domain ex: 'http://www.example.com')

In urls add:
url(r'^ipn_handler/', include('amazon_buttons.urls'))

It is also recomended for security that you enable AMAZON_IPN_VERIFY which will make sure that IPN's are authentic.  This requires signatures enabled on your form, as well as the ability to send outbound http requests from the server.

IPN responses will be saved and are viewable through the admin.



Signaling:

Ipns will trigger a save() action for the ipn model, and can thus be called via Django signaling. The model name is amazonbuttons.models.ipn_response


Example:
(the following can be placed anywhere in your project as long as it is imported at some point)

	import amazon_buttons.models
	from django.dispatch import receiver
	from django.db.models.signals import post_save


	@receiver(post_save, sender=amazon_buttons.models.ipn_response)
	def it_works(sender, instance, signal, *args, **kwargs):
		print str(instance.transactionId) + ' was completed successfully'







	







 
