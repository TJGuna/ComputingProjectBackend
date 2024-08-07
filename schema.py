import graphene
from graphql_jwt.decorators import login_required

from users.schema import Query as users_Query, Mutation as users_Mutation


class Query(users_Query, graphene.ObjectType):
    protected_data = graphene.String()

    @login_required
    def resolve_protected_data(self, info):
        return "This is protected data"


class Mutation(users_Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
