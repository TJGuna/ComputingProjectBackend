import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=False)
        role = graphene.String(required=True)

    def mutate(self, info, username, password, email=None, role='Client'):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        # Assign role
        if role == 'Admin':
            group = Group.objects.get(name='Admin')
        elif role == 'Expert':
            group = Group.objects.get(name='Expert')
        else:
            group = Group.objects.get(name='Client')

        user.groups.add(group)
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)