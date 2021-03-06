from django.db import models


# IPN Response

class ipn_response(models.Model):
	status = models.CharField(max_length = 100, default='empty')
	paymentReason = models.CharField(max_length = 300, default='empty')
	operation = models.CharField(max_length=200, default='empty')
	datetime =  models.DateTimeField('date published')
	buyerEmail = models.EmailField(max_length=200, default='empty@empty.com')
	recipientEmail = models.EmailField(max_length=200, default='empty@empty.com')
	referenceId = models.CharField(max_length=200, default='empty')
	buyerName = models.CharField(max_length=200, default='empty')
	recipientName = models.CharField(max_length=200, default='empty')
	transactionId = models.CharField(max_length=300, default='empty')
	paymentMethod = models.CharField(max_length=50, default='empty')
	transactionAmount = models.CharField(max_length=50, default='empty')
	ver_choice = (
        ('unverified', 'unverified'),
        ('verified', 'verified'),
        ('FLAG', 'FLAG'),
    	)
	ver_status = models.CharField(max_length=50, default='unverified', choices=ver_choice)
	def __unicode__(self):  
        	return self.status + ' ' + self.datetime.strftime("%b %d %Y %H:%M") + ' ' + self.ver_status 
		



