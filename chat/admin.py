# chat/admin.py
from django.contrib import admin
from .models import ChatRoom, Message

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'expert', 'created_at')
    search_fields = ('user__username', 'expert__username')
    list_filter = ('created_at',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'sender', 'content', 'timestamp')
    search_fields = ('chat_room__id', 'sender__username', 'content')
    list_filter = ('timestamp',)

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)