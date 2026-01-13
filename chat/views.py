"""
Chat views: Chat room list and individual chat
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import role_required
from .models import ChatRoom, Message
from accounts.models import User


@role_required(['donor', 'bloodbank', 'patient'])
def chat_list(request):
    """List all chat rooms for the current user"""
    # Get all chat rooms where user is a participant
    chat_rooms = ChatRoom.objects.filter(
        Q(participant1=request.user) | Q(participant2=request.user)
    ).select_related('participant1', 'participant2').order_by('-updated_at')
    
    # Get last message for each room
    rooms_with_last_message = []
    for room in chat_rooms:
        last_message = Message.objects.filter(room=room).order_by('-timestamp').first()
        other_user = room.get_other_participant(request.user)
        
        rooms_with_last_message.append({
            'room': room,
            'other_user': other_user,
            'last_message': last_message,
        })
    
    context = {
        'chat_rooms': rooms_with_last_message,
    }
    
    return render(request, 'chat/chat_list.html', context)


@role_required(['donor', 'bloodbank', 'patient'])
def chat_room(request, user_id):
    """Open or create a chat room with another user"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Don't allow chatting with yourself
    if other_user == request.user:
        messages.error(request, 'You cannot chat with yourself.')
        return redirect('chat:chat_list')
    
    # Get or create chat room
    room, created = ChatRoom.get_or_create_room(request.user, other_user)
    
    # Get messages for this room
    messages_list = Message.objects.filter(room=room).select_related('sender', 'receiver').order_by('timestamp')
    
    context = {
        'room': room,
        'other_user': other_user,
        'messages': messages_list,
    }
    
    return render(request, 'chat/chat_room.html', context)

