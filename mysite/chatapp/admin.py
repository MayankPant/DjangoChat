from django.contrib import admin
from .models import ChatRoom, ChatMessages
# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(ChatMessages)