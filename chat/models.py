"""
Chat models: ChatRoom and Message for real-time messaging
"""
from django.db import models
from accounts.models import User


class ChatRoom(models.Model):
    """
    Chat room between two users
    """
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_as_participant1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_as_participant2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
        unique_together = ['participant1', 'participant2']
    
    def __str__(self):
        return f"{self.participant1.username} <-> {self.participant2.username}"
    
    @classmethod
    def get_or_create_room(cls, user1, user2):
        """Get or create a chat room between two users"""
        # Ensure consistent ordering (smaller ID first)
        if user1.id > user2.id:
            user1, user2 = user2, user1
        
        room, created = cls.objects.get_or_create(
            participant1=user1,
            participant2=user2
        )
        return room, created
    
    def get_other_participant(self, user):
        """Get the other participant in the room"""
        if self.participant1 == user:
            return self.participant2
        return self.participant1


class Message(models.Model):
    """
    Message in a chat room
    """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:50]}"

