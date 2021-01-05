from django.contrib import admin
from accounts.models import User,Customer,Broker,connection,Review,Chat,Notify
# Register your models here.


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Broker)
admin.site.register(connection)
admin.site.register(Review)
admin.site.register(Chat)
admin.site.register(Notify)