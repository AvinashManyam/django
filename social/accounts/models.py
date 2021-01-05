from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db.models.signals import post_save
from multiselectfield import MultiSelectField
#Create your models here.

class User(AbstractUser):
    phone_number=models.PositiveIntegerField(default=0)
    is_customer=models.BooleanField(default=False)
    is_broker=models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Broker(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    department_name=models.CharField(max_length=30,default='NA')
    location=models.CharField(max_length=30,default='india')
    work= MultiSelectField()
    avg_rating=models.FloatField(default=0.0)
    rated_cust=models.IntegerField(default=0)
    profile_pic=models.ImageField(upload_to='profile_pics',default='profile_pic/nan1.jpg')
    city=models.CharField(max_length=30,default='NA',blank=True)
    firstname=models.CharField(max_length=10,default='NA',blank=True)
    lastname=models.CharField(max_length=10,default='NA',blank=True)
    def __str__(self):
        return self.user.__str__()

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    service_providers=models.ManyToManyField(Broker,through='connection')
    profile_pic=models.ImageField(upload_to='profile_pics',default='profile_pic/nan1.jpg')
    location=models.CharField(max_length=30,default='india')
    city=models.CharField(max_length=30,default='NA')
    firstname=models.CharField(max_length=10,default='NA')
    lastname=models.CharField(max_length=10,default='NA')
    def __str__(self):
        return self.user.__str__()


class connection(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="present_customer")
    broker=models.ForeignKey(Broker,on_delete=models.CASCADE,related_name="present_broker")
    description=models.CharField(max_length=250,null=True)
    customer_status=models.CharField(max_length=30)
    broker_status=models.CharField(max_length=30)
    status=models.IntegerField(default=0)
    created_time=models.DateTimeField(null=True)
    modified_time=models.DateTimeField(null=True)

class Review(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="present_cust")
    broker=models.ForeignKey(Broker,on_delete=models.CASCADE,related_name="present_bro")
    description=models.CharField(max_length=250,null=True)
    rating=models.IntegerField(default=0)

class Chat(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="present_c",default=None)
    broker=models.ForeignKey(Broker,on_delete=models.CASCADE,related_name="present_b",default=None)
    message = MultiSelectField()
    name=MultiSelectField(default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

class Notify(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    message = MultiSelectField(default=None)
    read=MultiSelectField(default=None)

