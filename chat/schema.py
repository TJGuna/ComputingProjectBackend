# chat/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoomType(DjangoObjectType):
    class Meta:
        model = ChatRoom
        fields = ('id', 'user', 'expert', 'created_at', 'messages')

    messages = graphene.List(lambda: MessageType)

    def resolve_messages(self, info):
        return self.messages.all()

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = ('id', 'chat_room', 'sender', 'content', 'timestamp')

class Query(graphene.ObjectType):
    chat_rooms = graphene.List(ChatRoomType, user_id=graphene.Int(required=True))
    messages = graphene.List(MessageType, chat_room_id=graphene.Int(required=True))

    def resolve_chat_rooms(self, info, user_id):
        return ChatRoom.objects.filter(user_id=user_id) | ChatRoom.objects.filter(expert_id=user_id)

    def resolve_messages(self, info, chat_room_id):
        return Message.objects.filter(chat_room_id=chat_room_id)

class CreateChatRoom(graphene.Mutation):
    chat_room = graphene.Field(ChatRoomType)

    class Arguments:
        user_id = graphene.Int(required=True)
        expert_id = graphene.Int(required=True)

    def mutate(self, info, user_id, expert_id):
        user = User.objects.get(id=user_id)
        expert = User.objects.get(id=expert_id)
        chat_room = ChatRoom(user=user, expert=expert)
        chat_room.save()
        return CreateChatRoom(chat_room=chat_room)

class CreateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        chat_room_id = graphene.Int(required=True)
        sender_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, chat_room_id, sender_id, content):
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        sender = User.objects.get(id=sender_id)
        message = Message(chat_room=chat_room, sender=sender, content=content)
        message.save()
        return CreateMessage(message=message)

class Mutation(graphene.ObjectType):
    create_chat_room = CreateChatRoom.Field()
    create_message = CreateMessage.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)