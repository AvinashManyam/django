from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,DetailView,CreateView,FormView,UpdateView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from accounts.models import Customer,Broker,User,connection,Review,Chat,Notify
from accounts.forms import userform,brokerform,searchform,BrokerEdit,CustomerEdit
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings 
from django.core.mail import send_mail
from itertools import chain
from django.contrib import messages
class HomePage(TemplateView):
    template_name='accounts/homepage.html'
def BHomePage(request):
    if request.method=='POST':
        if 'clear' in request.POST:
            broker=Broker.objects.get(user=request.user)
            Notify.objects.filter(user=broker.user).delete()
            print('Hellobro wassup')
    try:
        broker=Broker.objects.get(user=request.user)
    except:
        broker=None
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=broker.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'broker':broker,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',

    }
    return render(request,'broker/home.html',context=context)
def CHomePage(request):
    return render(request,'customer/home.html') 


def brokerauth(user):
    return user.is_broker


def isbroker(fn=None,login_url="accounts:broker_login"):
    decorator=user_passes_test(brokerauth)
    if fn:
        return decorator(fn)
    return decorator


def brokerlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active and user.is_broker:
                login(request,user)
                return redirect("accounts:Bhome")

            elif user.is_customer:
                return redirect("accounts:customer_login")

            else :
                return HttpResponseRedirect(reverse('accounts:broker_login'))

        else :
            print("failed login")
            print("username is"+username)
            print("password is"+password)
            return HttpResponseRedirect(reverse('accounts:broker_login'))

    else :
        return render(request,'broker/login.html')
def brokersignup(request):
    registered=False

    if request.method=='POST':
        user_form=userform(data=request.POST)
        broker_form=brokerform(data=request.POST)

        if user_form.is_valid() and broker_form.is_valid() :

            user=user_form.save()
            user.is_broker=True
            user.save()
            
            broker=broker_form.save(commit=False)
            broker.user=user
            broker.save()
            registered=True
        else:
            print(user_form.errors)
            print(broker_form.errors)

    else:

        user_form=userform()
        broker_form=brokerform()
    if registered:

        return HttpResponseRedirect(reverse('accounts:broker_login'))
    return render(request,'broker/signup.html',{'registered':registered,
                                                'userform':user_form ,
                                                'brokerform':broker_form})
class brokerdetail(DetailView):
    template_name="broker/home.html"
    model=User
def customerauth(user):
    return user.is_customer

def iscustomer(fn=None,redirect_field_name="app1:customer_login",login_url="app1:customer_login"):
    decorator=user_passes_test(customerauth)
    if fn:
        return decorator(fn)
    return decorator

def customerlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active and user.is_customer:
                login(request,user)
                return redirect("accounts:customer_home")
            
            elif user.is_broker:
                return redirect("accounts:broker_login")

            else :
                return HttpResponseRedirect(reverse('accounts:customer_login'))

        else :
            print("failed login")
            print("username is"+username)
            print("password is"+password)
            return HttpResponseRedirect(reverse('accounts:customer_login'))

    else :
        return render(request,'customer/login.html')    

def customersignup(request):
    registered=False

    if request.method=='POST':
        user_form=userform(data=request.POST)


        if user_form.is_valid() :

            user=user_form.save()
            user.is_customer=True
            user.save()
            customer=Customer()
            customer.user=user
            customer.save()
            registered=True
            subject='Registration Successfull'
            message=f'Hi {customer.user.username},You are successfully registered.Thanks for registering Hope.You have bright future in future'
            email_from=settings.EMAIL_HOST_USER
            reciept_list=[customer.user.email,]
            print(message)
            send_mail( subject, message, email_from, reciept_list ) 

        else:
            print(user_form.errors)

    else:

        user_form=userform()
    if registered:
        return HttpResponseRedirect(reverse('accounts:customer_login'))
    return render(request,'customer/signup.html',{'registered':registered,
                                                        'userform':user_form })
@login_required
def brokreview(request,pk):
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    presentcustomer=Customer.objects.get(user=request.user)
    orderslist=connection.objects.filter(customer=presentcustomer,status=1)
    context={
        "orders":orderslist,
    }
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    presentcustomer=Customer.objects.get(user=request.user)
    broker=Broker.objects.get(pk=pk)
    orderslist=connection.objects.filter(broker=broker)
    reviewlist=Review.objects.filter(broker=broker)
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        'broker':broker,
        "orders":orderslist,
        'review':reviewlist,
    }
    return render(request,'customer/brokreview.html',context=context)
@login_required
@iscustomer
def customerdetail(request):
    brokers=Broker.objects.all()
    if request.method=='POST':
        if "connect" in request.POST:
            newconnection=connection()
            presentbroker=Broker.objects.get(user__username=request.POST.get("broker"))
            presentcustomer=Customer.objects.get(user=request.user)
            orderslist=connection.objects.filter(customer=presentcustomer,status=1,broker=presentbroker)
            newconnection.broker=presentbroker
            newconnection.description=request.POST['description']
            print(newconnection.description)
            newconnection.customer=presentcustomer
            newconnection.customer_status="order pending"
            newconnection.broker_status="order not accepted"
            newconnection.created_time=timezone.now()
            newconnection.modified_time=timezone.now()
            newconnection.status=1
            if len(orderslist)==0:
                connection.objects.filter(customer=presentcustomer,status=3,broker=presentbroker).delete()
                connection.objects.filter(customer=presentcustomer,status=5,broker=presentbroker).delete()
                orderslist=connection.objects.filter(customer=presentcustomer,status=2,broker=presentbroker)
                if len(orderslist)==0:
                    newconnection.save()
                    subject='Request Pending'
                    message=f'Hi {presentbroker.user.username},someone requested to accept his approval'
                    email_from=settings.EMAIL_HOST_USER
                    reciept_list=[presentbroker.user.email,]
                    send_mail( subject, message, email_from, reciept_list ) 
                    chatlist1=Notify.objects.filter(user=presentbroker.user)
                    if len(chatlist1)==0:
                        newchat1=Notify()
                        newchat1.user=presentbroker.user
                        msg=f'{presentcustomer.user.username} Requested you to accept his order'
                        newchat1.message=[msg]
                        newchat1.read=['Request']
                        newchat1.save()
                        print('hello')
                        print(newchat1.message)
                    else:
                        oldchat1=Notify.objects.filter(user=presentbroker.user).first()
                        msg=f'{presentcustomer.user.username} : Requested you to accept his order'
                        list1=[msg]
                        list1.append(oldchat1.message)
                        oldchat1.message=list1
                        list1=['Request']
                        list1.append(oldchat1.read)
                        oldchat1.read=list1
                        oldchat1.save()
                        print(oldchat1.message)
            # print(message)

        elif 'search' in request.POST:
           
            department=request.POST.get('department')
            location=request.POST.get('location')
            some_var = request.POST.getlist('checks[]')
            list2=[]
            # brokers=Broker.objects.filter(department_name__startswith=department).filter(location__startswith=location)#.filter(work__contains=some_var[0])
            for o in some_var:
                list1=Broker.objects.filter(department_name__startswith=department).filter(location__startswith=location).filter(work__contains=o)
                list2=list(chain(list1,list2))
            brokers=list2
            brokers = list(set(brokers))
        elif 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'brokers':brokers,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
    }
    # Notify.objects.filter(user=customer.user).delete()
    return render(request,"customer/home.html",context)

@login_required
def Customerrequests(request):
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    presentcustomer=Customer.objects.get(user=request.user)
    orderslist=connection.objects.filter(customer=presentcustomer,status=1)
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "orders":orderslist,
    }
    # Notify.objects.filter(user=customer.user).delete()
    return render(request,"customer/custreq.html",context=context)
@login_required
def Customeraccepts(request):
    presentcustomer=Customer.objects.get(user=request.user)
    orderslist=connection.objects.filter(customer=presentcustomer,status=2)
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "orders":orderslist,
    }
    # Notify.objects.filter(user=customer.user).delete()
    return render(request,"customer/custacep.html",context=context)
@login_required
def Customerrejects(request):
    presentcustomer=Customer.objects.get(user=request.user)
    orderslist=connection.objects.filter(customer=presentcustomer,status=3)
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "orders":orderslist,
    }
    # Notify.objects.filter(user=customer.user).delete()
    return render(request,"customer/custrej.html",context=context)
@login_required
@iscustomer
def customerorders(request):
    presentcustomer=Customer.objects.get(user=request.user)
    orderslist=connection.objects.filter(customer=presentcustomer)
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "orders":orderslist,
    }
    # Notify.objects.filter(user=customer.user).delete()
    return render(request,"customer/orders.html",context=context)

@login_required
def Customercomplete(request):
    presentcustomer=Customer.objects.get(user=request.user)
    orderslist=connection.objects.filter(customer=presentcustomer,status=5)
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "orders":orderslist,
    }
    # Notify.objects.filter(user=customer.user).delete()
    return render(request,"customer/custcomp.html",context=context)

@login_required
def review(request,pk):
    presentcustomer=Customer.objects.get(user=request.user)
    broker=Broker.objects.get(pk=pk)
    orderslist=connection.objects.filter(customer=presentcustomer,broker=broker).first()
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    if request.method=='POST':
        if "submit" in request.POST:
            rating=request.POST['rating']
            description=request.POST['description']
            print(description)
            print(rating)
            if rating>='1' and rating<='5':
                reviewlist=Review.objects.filter(customer=presentcustomer,broker=broker)
                if len(reviewlist)==0:
                    newreview=Review()
                    newreview.broker=broker
                    newreview.customer=presentcustomer
                    newreview.rating=rating
                    newreview.description=description
                    newreview.save()
                    x=broker.avg_rating
                    broker.avg_rating=((x*broker.rated_cust)+float(rating))/(float(broker.rated_cust+1))
                    broker.rated_cust+=1
                    broker.save()
                else:
                    reviewlist=reviewlist.first()
                    x=broker.avg_rating
                    try:
                        broker.avg_rating=((x*broker.rated_cust)-reviewlist.rating)/(float(broker.rated_cust-1))
                    except:
                        broker.avg_rating=0
                    broker.rated_cust-=1
                    reviewlist.delete()
                    newreview=Review()
                    newreview.broker=broker
                    newreview.customer=presentcustomer
                    newreview.rating=rating
                    newreview.description=description
                    newreview.save()
                    x=broker.avg_rating
                    broker.avg_rating=((x*broker.rated_cust)+float(rating))/(float(broker.rated_cust+1))
                    broker.rated_cust+=1
                    broker.save()
            else:
                messages.error(request, 'Rating should be between 1 and 5')
    reviewlist=Review.objects.filter(customer=presentcustomer,broker=broker).first()
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        'customer':presentcustomer,
        'broker':broker,
        "orders":orderslist,
        'review':reviewlist,
    }
    return render(request,'customer/custreview.html',context=context)
@login_required
@isbroker
@csrf_exempt
def brokerrequests(request):
    presentbroker=Broker.objects.get(user=request.user)
    requestslist=connection.objects.filter(broker=presentbroker,status=1)
    if request.method=='POST':
        if 'clear' in request.POST:
            broker=Broker.objects.get(user=request.user)
            Notify.objects.filter(user=broker.user).delete()
            print('Hellobro wassup')
    try:
        broker=Broker.objects.get(user=request.user)
    except:
        broker=None
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=broker.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'broker':broker,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "requests":requestslist,

    }
    if request.method=='POST':
        presentconnection=connection.objects.filter(pk=request.POST.get("connection")).first()
        print(type(presentconnection))
        print(request.POST.get("connection"))
        if "accept" in request.POST and presentconnection is not None:
            presentconnection.customer_status="order accepted"
            presentconnection.broker_status="request accepted"
            presentconnection.modified_time=timezone.now()
            presentconnection.status=2
            presentconnection.save()
            subject='Request Accepted'
            message=f'Hi {presentconnection.customer.user.username},Your request is accepted by {presentbroker.user.username}'
            email_from=settings.EMAIL_HOST_USER
            reciept_list=[presentconnection.customer.user.email,]
            print(message)
            send_mail( subject, message, email_from, reciept_list ) 
            chatlist=Notify.objects.filter(user=presentconnection.customer.user)
            if len(chatlist)==0:
                newchat=Notify()
                newchat.user=presentconnection.customer.user
                msg=f'Your request is accepted by {presentbroker.user.username}'
                newchat.message=[msg]
                newchat.read=['Accept']
                newchat.save()
                print(newchat.message)
            else:
                oldchat=Notify.objects.filter(user=presentconnection.customer.user).first()
                msg=f'Your request is accepted by {presentbroker.user.username}'
                oldchat.message.append(msg)
                oldchat.read.append('Accept')
                oldchat.save()
            return render(request,"broker/requests.html",context=context)
        elif "reject" in request.POST and presentconnection is not None:
            presentconnection.customer_status="order rejected"
            presentconnection.broker_status="request rejected"
            presentconnection.modified_time=timezone.now()
            presentconnection.status=3
            presentconnection.save()
            subject='Request Rejected'
            message=f'Hi {presentconnection.customer.user.username},Your request is rejected by {presentbroker.user.username}.sorry to say this please try another broker'
            email_from=settings.EMAIL_HOST_USER
            reciept_list=[presentconnection.customer.user.email,]
            print(message)
            send_mail( subject, message, email_from, reciept_list )
            chatlist=Notify.objects.filter(user=presentconnection.customer.user)
            if len(chatlist)==0:
                newchat=Notify()
                newchat.user=presentconnection.customer.user
                msg=f'Your request is rejected by {presentbroker.user.username}'
                newchat.message=[msg]
                newchat.read=['Reject']
                newchat.save()
                print(newchat.message)
            else:
                oldchat=Notify.objects.filter(user=presentconnection.customer.user).first()
                msg=f'Your request is rejected by {presentbroker.user.username}'
                oldchat.message.append(msg)
                oldchat.read.append('Reject')
                oldchat.save() 
            return render(request,"broker/requests.html",context=context)
        else:
            return render(request,"broker/requests.html",context=context)
        
    
    return render(request,"broker/requests.html",context=context)

@login_required
def Brokeraccepts(request):
    presentbroker=Broker.objects.get(user=request.user)
    orderslist=connection.objects.filter(broker=presentbroker,status=2)
    if request.method=='POST':
        if 'clear' in request.POST:
            broker=Broker.objects.get(user=request.user)
            Notify.objects.filter(user=broker.user).delete()
            print('Hellobro wassup')
    try:
        broker=Broker.objects.get(user=request.user)
    except:
        broker=None
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=broker.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'broker':broker,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "orders":orderslist,

    }
    if request.method=='POST':
        presentconnection=connection.objects.filter(pk=request.POST.get("connection")).first()
        print(type(presentconnection))
        print(request.POST.get("connection"))
        if "completed" in request.POST and presentconnection is not None:
            presentconnection.customer_status="order completed"
            presentconnection.broker_status="request completed"
            presentconnection.modified_time=timezone.now()
            presentconnection.status=5
            presentconnection.save()
            Chat.objects.filter(broker=presentbroker,customer=presentconnection.customer).delete()
            subject='Request completed'
            message=f'Hi {presentconnection.customer.user.username},Your request is completed by {presentbroker.user.username}'
            email_from=settings.EMAIL_HOST_USER
            reciept_list=[presentconnection.customer.user.email,]
            print(message)
            send_mail( subject, message, email_from, reciept_list ) 
            chatlist=Notify.objects.filter(user=presentconnection.customer.user)
            if len(chatlist)==0:
                newchat=Notify()
                newchat.user=presentconnection.customer.user
                msg=f'Your request is completed by {presentbroker.user.username}'
                newchat.message=[msg]
                newchat.read=['Complete']
                newchat.save()
                print(newchat.message)
            else:
                oldchat=Notify.objects.filter(user=presentconnection.customer.user).first()
                msg=f'Your request is completed by {presentbroker.user.username}'
                oldchat.message.append(msg)
                oldchat.read.append('Complete')
                oldchat.save()
            return render(request,"broker/brokacep.html",context=context)
        elif "reject" in request.POST and presentconnection is not None:
            presentconnection.customer_status="order rejected"
            presentconnection.broker_status="request rejected"
            presentconnection.modified_time=timezone.now()
            presentconnection.status=3
            presentconnection.save()
            subject='Request Rejected'
            Chat.objects.filter(broker=presentbroker,customer=presentconnection.customer).delete()
            message=f'Hi {presentconnection.customer.user.username},Your request is rejected by {presentbroker.user.username}.sorry to say this please try another broker'
            email_from=settings.EMAIL_HOST_USER
            reciept_list=[presentconnection.customer.user.email,]
            print(message)
            send_mail( subject, message, email_from, reciept_list ) 
            chatlist=Notify.objects.filter(user=presentconnection.customer.user)
            if len(chatlist)==0:
                newchat=Notify()
                newchat.user=presentconnection.customer.user
                msg=f'Your request is rejected by {presentbroker.user.username}'
                newchat.message=[msg]
                newchat.read=['Reject']
                newchat.save()
                print(newchat.message)
            else:
                oldchat=Notify.objects.filter(user=presentconnection.customer.user).first()
                msg=f'Your request is rejected by {presentbroker.user.username}'
                oldchat.message.append(msg)
                oldchat.read.append('Reject')
                oldchat.save()
            return render(request,"broker/brokacep.html",context=context)
        else:
            return render(request,"broker/brokacep.html",context=context)
    return render(request,"broker/brokacep.html",context=context)
@login_required
def Brokerrrejects(request):
    presentbroker=Broker.objects.get(user=request.user)
    orderslist=connection.objects.filter(broker=presentbroker,status=3)
    if request.method=='POST':
        if 'clear' in request.POST:
            broker=Broker.objects.get(user=request.user)
            Notify.objects.filter(user=broker.user).delete()
            print('Hellobro wassup')
    try:
        broker=Broker.objects.get(user=request.user)
    except:
        broker=None
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=broker.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'broker':broker,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "orders":orderslist,

    }
    if request.method=='POST':
        presentconnection=connection.objects.filter(pk=request.POST.get("connection")).first()
        print(type(presentconnection))
        print(request.POST.get("connection"))
        if "clear" in request.POST and presentconnection is not None:
            presentconnection.delete()
            return render(request,"broker/brokrej.html",context=context)
        elif 'clearpage' in request.POST:
            connection.objects.filter(broker=presentbroker,status=3).delete()
            return render(request,"broker/brokrej.html",context=context)
    print(len(orderslist))
    return render(request,"broker/brokrej.html",context=context)
@login_required
def Brokercomplete(request):
    presentbroker=Broker.objects.get(user=request.user)
    orderslist=connection.objects.filter(broker=presentbroker,status=5)
    if request.method=='POST':
        if 'clear' in request.POST:
            broker=Broker.objects.get(user=request.user)
            Notify.objects.filter(user=broker.user).delete()
            print('Hellobro wassup')
    try:
        broker=Broker.objects.get(user=request.user)
    except:
        broker=None
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=broker.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'broker':broker,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
        "orders":orderslist,

    }
    return render(request,"broker/brokcomp.html",context=context)
@login_required
def BrokerProfileView(request):
    if request.method=='POST':
        if 'clear' in request.POST:
            broker=Broker.objects.get(user=request.user)
            Notify.objects.filter(user=broker.user).delete()
            print('Hellobro wassup')
    try:
        broker=Broker.objects.get(user=request.user)
    except:
        broker=None
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=broker.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'broker':broker,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',

    }
    return render(request,'broker/profile.html',context=context)

@login_required
def BrokerProfileEditView(request):
    form = BrokerEdit()
    if request.method == 'POST':
        if 'clear' in request.POST:
            broker=Broker.objects.get(user=request.user)
            Notify.objects.filter(user=broker.user).delete()
            print('Hellobro wassup')
        else:
            form=BrokerEdit(request.POST)
            if form.is_valid:
                user=request.user
                firstname=request.POST['firstname']
                lastname=request.POST['lastname']
                city=request.POST['city']
                location=request.POST['location']
                department_name=request.POST['department_name']
                phone_number=request.POST['phone_number']
                try:
                    profile_pic=request.FILES['profile_pic']
                except MultiValueDictKeyError:
                    profile_pic=False
                email=request.POST['email']
                some_var = request.POST.getlist('checks[]')
                broker=Broker.objects.get(user=user)
                if firstname:
                    broker.firstname=firstname
                if lastname:
                    broker.lastname=lastname
                if city:
                    broker.city=city
                if location:
                    broker.location=location
                if department_name:
                    broker.department_name=department_name
                if phone_number:
                    broker.user.phone_number=phone_number
                if profile_pic:
                    broker.profile_pic=profile_pic
                if email:
                    broker.user.email=email
                if some_var:
                    broker.work=some_var
                broker.save()
                broker.user.save()
                print(broker.work)
                return redirect('accounts:brokerprofile')
    broker=Broker.objects.get(user=request.user)
    try:
        broker=Broker.objects.get(user=request.user)
    except:
        broker=None
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=broker.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'broker':broker,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',

    }
    return render(request,'broker/profile_edit.html',context=context)

@login_required
def CustomerProfileView(request):
    customer=Customer.objects.get(user=request.user)
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
    }
    return render(request,'customer/profile.html',context=context)

@login_required
def CustomerProfileEditView(request):
    form = CustomerEdit()
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    if request.method == 'POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
        else:
            form=CustomerEdit(request.POST)
            if form.is_valid:
                user=request.user
                firstname=request.POST['firstname']
                lastname=request.POST['lastname']
                city=request.POST['city']
                location=request.POST['location']
                phone_number=request.POST['phone_number']
                try:
                    profile_pic=request.FILES['profile_pic']
                except MultiValueDictKeyError:
                    profile_pic=False
                customer=Customer.objects.get(user=user)
                email=request.POST['email']
                if firstname:
                    customer.firstname=firstname
                if lastname:
                    customer.lastname=lastname
                if city:
                    customer.city=city
                if location:
                    customer.location=location
                if phone_number:
                    customer.user.phone_number=phone_number
                if profile_pic:
                    customer.profile_pic=profile_pic
                if email:
                    customer.user.email=email
                customer.save()
                customer.user.save()
                #print(customer.profile_pic)
                return redirect('accounts:customerprofile')
    customer=Customer.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    customer=Customer.objects.get(user=request.user)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
    }
    return render(request,'customer/profile_edit.html',context=context)


def brokchat(request,pk):
    if request.method=='POST':
        if 'clear' in request.POST:
            broker=Broker.objects.get(user=request.user)
            Notify.objects.filter(user=broker.user).delete()
            print('Hellobro wassup')
    try:
        broker=Broker.objects.get(user=request.user)
    except:
        broker=None
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=broker.user).first().read
        readlist.reverse()
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'broker':broker,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',

    }
    customer=Customer.objects.get(pk=pk)
    chatlist=Chat.objects.filter(broker=broker,customer=customer)
    if request.method=='POST':
        if 'enter' in request.POST:
            description=request.POST['description']
            if len(chatlist)==0:
                newchat=Chat()
                newchat.broker=broker
                newchat.customer=customer
                if description:
                    newchat.message=[description]
                    newchat.name=broker.user.username
                    newchat.timestamp=timezone.now()
                    newchat.save()
                    # context['message']=newchat.message
            else:
                oldchat=Chat.objects.filter(broker=broker,customer=customer).first()
                if description:
                    oldchat.message.append(description)
                    oldchat.name.append(broker.user.username)
                    oldchat.save()
                    # context['message']=oldchat.message
            
            # print(msg)
            if description:
                chatlist1=Notify.objects.filter(user=customer.user)
                if len(chatlist1)==0:
                    newchat=Notify()
                    newchat.user=customer.user
                    msg=f'{broker.user.username} : {description}'
                    newchat.message=[msg]
                    newchat.read=['Chat']
                    newchat.save()
                    print(newchat.message)
                else:
                    oldchat=Notify.objects.filter(user=customer.user).first()
                    msg=f'{broker.user.username} : {description}'
                    oldchat.message.append(msg)
                    oldchat.read.append('Chat')
                    oldchat.save()

                # print(oldchat.broker)
            print(description)
        
    chatlist=Chat.objects.filter(broker=broker,customer=customer)
    try:
        chatmessage=Chat.objects.filter(broker=broker,customer=customer).first().message
    except:
        chatmessage=[]
    try:
        chatname=Chat.objects.filter(broker=broker,customer=customer).first().name
    except:
        chatname=[]
    zipedlist=zip(chatmessage,chatname)
    context['broker']=broker
    context['customer']=customer
    context['chat']=chatlist
    context['message']=zipedlist
    context['usr']=broker.user.username
    return render(request,'broker/chat.html',context=context)

def custchat(request,pk):
    customer=Customer.objects.get(user=request.user)
    if request.method=='POST':
        if 'clear' in request.POST:
            customer=Customer.objects.get(user=request.user)
            Notify.objects.filter(user=customer.user).delete()
            print('Hellobro wassup')
    try:
        chatlist=Notify.objects.filter(user=customer.user).first().message
        chatlist.reverse()
    except:
        chatlist=[]
    try:
        readlist=Notify.objects.filter(user=customer.user).first().read
        readlist.reverse
    except:
        readlist=[]
    totallist=zip(chatlist,readlist)
    context={
        'chathome':totallist,
        'customer':customer,
        'trail1':'Chat',
        'trail2':'Accept',
        'trail3':'Reject',
        'trail4':'Complete',
        'trail5':'Request',
    }
    broker=Broker.objects.get(pk=pk)
    chatlist=Chat.objects.filter(broker=broker,customer=customer)
    if request.method=='POST':
        if 'enter' in request.POST:
            description=request.POST['description']
            if len(chatlist)==0:
                newchat=Chat()
                newchat.broker=broker
                newchat.customer=customer
                if description:
                    newchat.message=[description]
                    newchat.name=customer.user.username
                    newchat.timestamp=timezone.now()
                    newchat.save()
                    context['message']=newchat.message
            else:
                oldchat=Chat.objects.filter(broker=broker,customer=customer).first()
                if description:
                    oldchat.message.append(description)
                    oldchat.name.append(customer.user.username)
                    oldchat.save()
                    context['message']=oldchat.message

                print(oldchat.broker)
            if description:
                chatlist1=Notify.objects.filter(user=broker.user)
                if len(chatlist1)==0:
                    newchat1=Notify()
                    newchat1.user=broker.user
                    msg=f'{customer.user.username} : {description}'
                    newchat1.message=[msg]
                    newchat1.read=['Chat']
                    newchat1.save()
                    print(newchat1.message)
                else:
                    oldchat1=Notify.objects.filter(user=broker.user).first()
                    msg=f'{customer.user.username} : {description}'
                    oldchat1.message.append(msg)
                    oldchat1.read.append('Chat')
                    oldchat1.save()
                    print(oldchat1.message)
            print(description)
        
    chatlist=Chat.objects.filter(broker=broker,customer=customer)
    try:
        chatmessage=Chat.objects.filter(broker=broker,customer=customer).first().message
    except:
        chatmessage=[]
    try:
        chatname=Chat.objects.filter(broker=broker,customer=customer).first().name
    except:
        chatname=[]
    zipedlist=zip(chatmessage,chatname)
    context['broker']=broker
    context['customer']=customer
    context['chat']=chatlist
    context['message']=zipedlist
    context['usr']=broker.user.username
    return render(request,'customer/chat.html',context=context)


@login_required
@iscustomer
def custnotify(request):
    print('hello bro')
    return render(request,'customer/base.html',context=context)

@login_required
@isbroker
def broknotify(request):
    broker=Broker.objects.get(user=request.user)
    try:
        chatlist=Notify.objects.filter(user=broker.user).first().message
    except:
        chatlist=[]
    context={
        'chat':chatlist,
        'broker':broker
    }
    # Notify.objects.filter(user=broker.user).delete()
    return render(request,'broker/notify.html',context=context)
