# accounts/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Define the UserType
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'role', 'date_of_birth', 'address', 'bio', 'profile_picture')

# Define the Queries
class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users_by_role = graphene.List(UserType, role=graphene.String(required=True))

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_users_by_role(self, info, role):
        return get_user_model().objects.filter(role=role)

# Define the Mutations
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        role = graphene.String(required=True)
        date_of_birth = graphene.Date()
        address = graphene.String()
        bio = graphene.String()
        profile_picture = graphene.String()

    def mutate(self, info, username, email, password, role, date_of_birth=None, address=None, bio=None, profile_picture=None):
        user = get_user_model()(
            username=username,
            email=email,
            role=role,
            date_of_birth=date_of_birth,
            address=address,
            bio=bio,
            profile_picture=profile_picture
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int(required=True)
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()
        role = graphene.String()
        date_of_birth = graphene.Date()
        address = graphene.String()
        bio = graphene.String()
        profile_picture = graphene.String()

    def mutate(self, info, id, username=None, email=None, password=None, role=None, date_of_birth=None, address=None, bio=None, profile_picture=None):
        user = get_user_model().objects.get(id=id)
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        if role:
            user.role = role
        if date_of_birth:
            user.date_of_birth = date_of_birth
        if address:
            user.address = address
        if bio:
            user.bio = bio
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = get_user_model().objects.get(id=id)
        user.delete()
        return DeleteUser(success=True)

class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    access_token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            raise Exception('Invalid username or password')
        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))
        return LoginUser(user=user, access_token=access_token, refresh_token=refresh_token)

class RefreshTokenMutation(graphene.Mutation):
    access_token = graphene.String()

    class Arguments:
        refresh_token = graphene.String(required=True)

    def mutate(self, info, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return RefreshTokenMutation(access_token=access_token)
        except Exception as e:
            raise Exception('Invalid refresh token')

class VerifyTokenMutation(graphene.Mutation):
    valid = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        token = graphene.String(required=True)

    def mutate(self, info, token):
        try:
            AccessToken(token)
            return VerifyTokenMutation(valid=True, message="Token is valid")
        except Exception as e:
            return VerifyTokenMutation(valid=False, message=str(e))

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login_user = LoginUser.Field()
    refresh_token = RefreshTokenMutation.Field()
    verify_token = VerifyTokenMutation.Field()

# Combine Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)