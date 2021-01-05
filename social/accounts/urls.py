from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views
from django.conf import settings 
from django.conf.urls.static import static 
from accounts.views import (brokerlogin,brokersignup,customerlogin,customersignup,customerdetail,brokerdetail,brokerrequests,customerorders,BrokerProfileView,
Brokeraccepts,Brokerrrejects,Customeraccepts,Customerrejects,review)
app_name='accounts'

urlpatterns = [
    url(r"^broker/$", views.BHomePage, name="Bhome"),
    url(r"^customer/$", views.CHomePage, name="Chome"),
    path('broker/login/',brokerlogin,name="broker_login"),
    path('broker/signup/',brokersignup,name="broker_signup"),
    path('customer/$',customerdetail,name="customer_home"),
    url(r'^logout/$',auth_views.LogoutView.as_view(template_name='accounts/homepage.html'),name='logout'),
    path('customer/login/',customerlogin,name="customer_login"),
    path('customer/signup/',customersignup,name="customer_signup"),
    path('broker/<int:pk>/',brokerdetail.as_view(),name="broker_home"),
    path('broker/requests/',brokerrequests,name="broker_requests"),
    path('customer/orders/',customerorders,name="customer_orders"),
    path('broker/profile/',views.BrokerProfileView,name='brokerprofile'),
    path('broker/profile/edit/',views.BrokerProfileEditView,name='brokerprofileedit'),
    path('customer/profile/',views.CustomerProfileView,name='customerprofile'),
    path('customer/profile/edit/',views.CustomerProfileEditView,name='customerprofileedit'),
    path('customer/orders/requests/',views.Customerrequests,name='Customerrequests'),
    path('customer/orders/accepts/',views.Customeraccepts,name='Customeraccepts'),
    path('customer/orders/rejects/',views.Customerrejects,name='Customerrejects'),
    path('customer/orders/completes/',views.Customercomplete,name='Customercompletes'),
    path('broker/orders/accepts/',views.Brokeraccepts,name='Brokeraccepts'),
    path('broker/orders/rejects/',views.Brokerrrejects,name='Brokerrejects'),
    path('broker/orders/completes/',views.Brokercomplete,name='Brokercompletes'),
    path('review/<int:pk>/',views.review,name="review"),
    path('customer/broker/review/<int:pk>/',views.brokreview,name="brokreview"),
    path('broker/chat/<int:pk>/',views.brokchat,name="brokchat"),
    path('customer/chat/<int:pk>/',views.custchat,name="custchat"),
    path('customer/notify/',views.custnotify,name="custnotify"),
    path('brok/notify/',views.broknotify,name="broknotify"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)