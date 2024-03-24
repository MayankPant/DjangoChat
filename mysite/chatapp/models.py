from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


    def __str__(self) -> str:
        return self.name
    

class ChatMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_content = models.TextField()
    date = models.DateTimeField(auto_now = True)


    class Meta:
        ordering=('date',) # used for ordering messages with respect to date
