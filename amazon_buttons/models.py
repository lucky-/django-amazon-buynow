from django.db import models

# IPN Response

class ipn_response(models.Model):
	status = models.CharField(max_length = 100)
	paymentReason = models.CharField(max_length = 300)
	operation = models.CharField(max_length=200)
	datetime =  models.DateTimeField('date published')
	buyerEmail = models.EmailField(max_length=200)
	recipientEmail = models.EmailField(max_length=200)
	referenceId = models.CharField(max_length=200)
	buyerName = models.CharField(max_length=200)
	recipientName = models.CharField(max_length=200)
	transactionId = models.CharField(max_length=300)
	paymentMethod = models.CharField(max_length=50)
	transactionAmount = models.CharField(max_length=50)
	def __unicode__(self):  
        	return self.status + ' ' + self.datetime.strftime("%b %d %Y %H:%M")
		



