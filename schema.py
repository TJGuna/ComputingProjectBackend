import graphene
from accounts.schema import Query as acc_Query, Mutation as acc_Mutation



class Query(acc_Query, graphene.ObjectType):
    protected_data = graphene.String()


    def resolve_protected_data(self, info):
        return "This is protected data"


class Mutation(acc_Mutation, graphene.ObjectType):
    pass





# schema = graphene.Schema(mutation=Mutation)


schema = graphene.Schema(query=Query, mutation=Mutation)
