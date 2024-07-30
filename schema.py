import graphene

from project.schema import Query as project_Query, Mutation as project_Mutation


class Query(project_Query, graphene.ObjectType):
    pass


class Mutation(project_Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
