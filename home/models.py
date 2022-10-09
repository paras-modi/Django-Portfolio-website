from django.db import models

# Create your models here.

class Person(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    message=models.TextField(max_length=250)

class Transaction(models.Model):

    made_on = models.DateTimeField(auto_now_add=True)

    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)