import graphene
from graphene_django.types import DjangoObjectType
from .models import User, Project, Task


# Define GraphQL types

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'created_by', 'team_members')


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'project', 'assigned_to', 'status')


# Define GraphQL Queries

class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    project_by_id = graphene.Field(ProjectType, id=graphene.Int(required=True))
    tasks_by_project = graphene.List(TaskType, project_id=graphene.Int(required=True))

    def resolve_all_projects(self, info, **kwargs):
        return Project.objects.all()

    def resolve_project_by_id(self, info, id):
        return Project.objects.get(id=id)

    def resolve_tasks_by_project(self, info, project_id):
        return Task.objects.filter(project_id=project_id)


# Define GraphQL Mutations

class CreateProject(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        start_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)
        created_by = graphene.Int(required=True)

    project = graphene.Field(ProjectType)

    def mutate(self, info, title, description, start_date, end_date, created_by):
        created_by_user = User.objects.get(id=created_by)
        project = Project(title=title, description=description, start_date=start_date, end_date=end_date,
                          created_by=created_by_user)
        project.save()
        return CreateProject(project=project)


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
