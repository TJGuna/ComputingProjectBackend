# schema.py
import graphene
import accounts.schema
import important_dates.schema
import chat.schema
import guides.schema

class Query(accounts.schema.Query, important_dates.schema.Query, chat.schema.Query, guides.schema.Query, graphene.ObjectType):
    pass

class Mutation(accounts.schema.Mutation, important_dates.schema.Mutation, chat.schema.Mutation, guides.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)