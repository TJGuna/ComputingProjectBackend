# important_dates/schema.py
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from .models import ImportantDate
import graphene

class ImportantDateType(DjangoObjectType):
    class Meta:
        model = ImportantDate
        fields = ('id', 'title', 'date', 'location', 'description', 'notes', 'user', 'created_at', 'updated_at')

class Query(graphene.ObjectType):
    important_dates = graphene.List(ImportantDateType)
    important_date = graphene.Field(ImportantDateType, id=graphene.Int(required=True))

    def resolve_important_dates(self, info):
        return ImportantDate.objects.all()

    def resolve_important_date(self, info, id):
        return ImportantDate.objects.get(id=id)

class CreateImportantDate(graphene.Mutation):
    important_date = graphene.Field(ImportantDateType)

    class Arguments:
        title = graphene.String(required=True)
        date = graphene.Date(required=True)
        location = graphene.String(required=True)
        description = graphene.String()
        notes = graphene.String()
        user_id = graphene.Int(required=True)

    def mutate(self, info, title, date, location, description=None, notes=None, user_id=None):
        user = get_user_model().objects.get(id=user_id)
        important_date = ImportantDate(
            title=title,
            date=date,
            location=location,
            description=description,
            notes=notes,
            user=user
        )
        important_date.save()
        return CreateImportantDate(important_date=important_date)

class UpdateImportantDate(graphene.Mutation):
    important_date = graphene.Field(ImportantDateType)

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        date = graphene.Date()
        location = graphene.String()
        description = graphene.String()
        notes = graphene.String()

    def mutate(self, info, id, title=None, date=None, location=None, description=None, notes=None):
        important_date = ImportantDate.objects.get(id=id)
        if title:
            important_date.title = title
        if date:
            important_date.date = date
        if location:
            important_date.location = location
        if description:
            important_date.description = description
        if notes:
            important_date.notes = notes
        important_date.save()
        return UpdateImportantDate(important_date=important_date)

class DeleteImportantDate(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        important_date = ImportantDate.objects.get(id=id)
        important_date.delete()
        return DeleteImportantDate(success=True)

class Mutation(graphene.ObjectType):
    create_important_date = CreateImportantDate.Field()
    update_important_date = UpdateImportantDate.Field()
    delete_important_date = DeleteImportantDate.Field()