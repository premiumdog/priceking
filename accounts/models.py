from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xml_link = models.CharField(max_length=140)
    credit = models.IntegerField(default=0, blank=True, null=True)
    profile_image = models.ImageField(blank=True)
    store_name = models.CharField(max_length=254, blank=True, default="")
    store_description = models.TextField(default="",blank=True)
    store_payments = models.CharField(max_length=254, blank=True, default="")
    store_order_method = models.CharField(max_length=254, blank=True, default="")
    store_delivery_method = models.CharField(max_length=254, blank=True, default="")
    store_location = models.CharField(max_length=254, blank=True, default="")
    tax_number = models.CharField(max_length=254, blank=True, default="")
    tax_number_eu = models.CharField(max_length=254, blank=True, default="")
    form_of_enterprise = models.CharField(max_length=254, blank=True, default="")
    store_registration_number = models.CharField(max_length=254, blank=True, default="")
    store_main_location = models.CharField(max_length=254, blank=True, default="")
    store_city = models.CharField(max_length=254, blank=True, default="")
    store_zip = models.CharField(max_length=254, blank=True, default="")
    store_street = models.CharField(max_length=254, blank=True, default="")
    store_contact_email = models.EmailField(blank=True, default="")
    store_contact_phone = models.CharField(max_length=254, blank=True, default="")

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username
