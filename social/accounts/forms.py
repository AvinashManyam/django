from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import User,Broker,Customer,connection
from multiselectfield import MultiSelectFormField

class userform(UserCreationForm):
    class Meta():
        model=User
        fields=('username','email',"phone_number")


class brokerform(forms.ModelForm):
    class Meta():
        model=Broker
        fields=('department_name','location')
class searchform(forms.ModelForm):
    class Meta():
        model=Broker
        fields=('department_name','location')

class BrokerEdit(forms.Form):
    firstname=forms.CharField(max_length=256,required=False)
    lastname=forms.CharField(max_length=256,required=False)
    city=forms.CharField(max_length=256,required=False)
    department_name=forms.CharField(max_length=256,required=False)
    location=forms.CharField(max_length=256,required=False)
    phone_number=forms.IntegerField(required=False)
    profile_pic=forms.ImageField(required=False)
    email=forms.EmailField(required=False)
    work= MultiSelectFormField(widget=forms.CheckboxSelectMultiple)

class CustomerEdit(forms.Form):
    firstname=forms.CharField(max_length=256,required=False)
    lastname=forms.CharField(max_length=256,required=False)
    city=forms.CharField(max_length=256,required=False)
    location=forms.CharField(max_length=256,required=False)
    phone_number=forms.IntegerField(required=False)
    profile_pic=forms.ImageField(required=False)
    email=forms.EmailField(required=False)
