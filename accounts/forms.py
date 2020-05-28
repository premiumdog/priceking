from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from shop.models import Product
from accounts.models import UserProfile
from django.utils.translation import gettext_lazy as _


ENTERPRISE_TYPE = (
    ("Társas vállalkozás", _("Társas vállalkozás")),
    ("Egyéni vállalkozás", _("Egyéni vállalkozás")),
    ("Társas vállalkozás adószámos", _("Társas vállalkozás adószámos")),
    ("Magánszemély", _("Magánszemély")),
    ("Egyéb szervezet", _("Egyéb szervezet"))
)

#Login form
class LoginForm(forms.Form):
    username = forms.CharField(label='Felhasználónév')
    password = forms.CharField(widget=forms.PasswordInput, label='Jelszó')


#Register form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Jelszó', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Jelszó újra', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {
            'username': _('Felhasználónév'),
            'first_name': _('Cég neve'),
            'email': _('E-mail cím'),
        }
        help_texts = {'username': "Példa: premiumdog",}


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('A jelszavak nem egyformák.')
        return cd['password2']




class CreateUserProfile(ModelForm):
    form_of_enterprise = forms.ChoiceField(choices = ENTERPRISE_TYPE, label="Vállakozás formája", initial='Kérem válasszon', widget=forms.Select(), required=True)
    class Meta:
        model = UserProfile
        fields = ['store_name','tax_number','form_of_enterprise','store_registration_number','store_location','store_main_location','store_zip','store_city','store_street','store_contact_email','store_contact_phone','profile_image']
        #exclude = ['tax_number','tax_number_eu','form_of_enterprise','store_registration_number','store_main_location','store_city','store_zip','store_street','store_contact_email','store_contact_phone']
        labels = {
            'profile_image': _('Logó'),
            'store_name': _('Megjelenítendő cég név (vállalkozási forma nélkül)'),
            'store_payments': _('Fizetési lehetőségek'),
            'store_order_method': _('Rendelési lehetőségek'),
            'store_delivery_method': _('Szállítási lehetőségek'),
            'store_location': _('Cég székhely'),
            'tax_number': _('Adószám'),
            'form_of_enterprise': _('Vállakozás formája'),
            'store_registration_number': _('Cégjegyzékszám'),
            'store_main_location': _('Ország'),
            'store_city': _('Város'),
            'store_zip': _('Irányítószám'),
            'store_street': _('Utca, házszám'),
            'store_registration_number': _('Cég nyilvántartási száma'),
            'store_contact_email': _('Kapcsolattartó e-mail cím'),
            'store_contact_phone': _('Kapcsolattartó telefonszám'),
        }
        help_texts = {'form_of_enterprise': "társas vállalkozás egyéni vállalkozás társas vállalkozás adószámos magánszemély egyéb szervezet",
        'store_name': "Példa: premiumDog.hu"}


class EditUserProfile(ModelForm):
    form_of_enterprise = forms.ChoiceField(choices = ENTERPRISE_TYPE, label="Vállakozás formája", initial='Kérem válasszon', widget=forms.Select(), required=True)
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user', 'credit']
        labels = {
            'profile_image': _('Logó'),
            'store_name': _('Megjelenítendő cég név (vállalkozási forma nélkül)'),
            'store_payments': _('Fizetési lehetőségek'),
            'store_order_method': _('Rendelési lehetőségek'),
            'store_delivery_method': _('Szállítási lehetőségek'),
            'store_location': _('Cég székhely'),
            'tax_number': _('Adószám'),
            'tax_number_eu': _('EU-s adószám'),
            'form_of_enterprise': _('Vállakozás formája'),
            'store_registration_number': _('Cégjegyzékszám'),
            'store_main_location': _('Ország'),
            'store_city': _('Város'),
            'store_zip': _('Irányítószám'),
            'store_street': _('Utca, házszám'),
            'store_registration_number': _('Cég nyilvántartási száma'),
            'store_contact_email': _('Kapcsolattartó e-mail cím'),
            'store_contact_phone': _('Kapcsolattartó telefonszám'),
            'store_description': _('Leírás'),
        }


class CreditForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['store_name','form_of_enterprise', 'tax_number','tax_number_eu','store_registration_number','store_location','store_main_location','store_city','store_zip','store_street','store_contact_email','store_contact_phone']
        labels = {
            'store_name': _('Megjelenítendő cég név (vállalkozási forma nélkül)'),
            'store_location': _('Cég székhely'),
            'tax_number': _('Adószám'),
            'tax_number_eu': _('EU-s adószám'),
            'form_of_enterprise': _('Vállakozás formája'),
            'store_registration_number': _('Cégjegyzékszám'),
            'store_main_location': _('Ország'),
            'store_city': _('Város'),
            'store_zip': _('Irányítószám'),
            'store_street': _('Utca, házszám'),
            'store_registration_number': _('Cég nyilvántartási száma'),
            'store_contact_email': _('Kapcsolattartó e-mail cím'),
            'store_contact_phone': _('Kapcsolattartó telefonszám'),
        }



