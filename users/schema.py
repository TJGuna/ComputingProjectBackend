# schema.py

import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
import logging

logger = logging.getLogger(__name__)


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class ObtainJSONWebToken(graphql_jwt.ObtainJSONWebToken):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class RefreshJSONWebToken(graphql_jwt.Refresh):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    refresh_token = RefreshJSONWebToken.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        logger.debug(f"Authenticated user: {user}")
        return user


schema = graphene.Schema(query=Query, mutation=Mutation)

