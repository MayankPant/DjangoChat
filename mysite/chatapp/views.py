from django.shortcuts import render
from .models import ChatRoom, ChatMessages
# Create your views here.

def index(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chatapp/index.html', {"chatrooms" : chatrooms})


def chatroom(request, slug):
    room = ChatRoom.objects.get(slug=slug)
    chat_messages = ChatMessages.objects.filter(room = room)
    return render(request, 'chatapp/room.html', {"chatroom" : room, "chat_messages" : chat_messages})
