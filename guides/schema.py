# guides/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from django.core.files.base import ContentFile
import base64

from guides.models import Guide


class GuideType(DjangoObjectType):
    class Meta:
        model = Guide
        fields = ('id', 'title', 'content', 'author', 'image', 'created_at', 'updated_at')

class Query(graphene.ObjectType):
    guides = graphene.List(GuideType)
    guide = graphene.Field(GuideType, id=graphene.Int(required=True))

    def resolve_guides(self, info):
        return Guide.objects.all()

    def resolve_guide(self, info, id):
        try:
            return Guide.objects.get(id=id)
        except Guide.DoesNotExist:
            return None

class CreateGuide(graphene.Mutation):
    guide = graphene.Field(GuideType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        image = graphene.String(required=False)  # Assuming image is a base64 encoded string

    def mutate(self, info, title, content, image=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        guide = Guide(title=title, content=content, author=user)

        if image:
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            guide.image = ContentFile(base64.b64decode(imgstr), name=f'{title}.{ext}')

        guide.save()
        return CreateGuide(guide=guide)

class UpdateGuide(graphene.Mutation):
    guide = graphene.Field(GuideType)

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=False)
        content = graphene.String(required=False)
        image = graphene.String(required=False)  # Assuming image is a base64 encoded string

    def mutate(self, info, id, title=None, content=None, image=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        try:
            guide = Guide.objects.get(id=id, author=user)
        except Guide.DoesNotExist:
            raise Exception("Guide not found or not authorized to update")

        if title:
            guide.title = title
        if content:
            guide.content = content
        if image:
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            guide.image = ContentFile(base64.b64decode(imgstr), name=f'{guide.title}.{ext}')

        guide.save()
        return UpdateGuide(guide=guide)

class DeleteGuide(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required!")

        try:
            guide = Guide.objects.get(id=id, author=user)
        except Guide.DoesNotExist:
            raise Exception("Guide not found or not authorized to delete")

        guide.delete()
        return DeleteGuide(success=True)

class Mutation(graphene.ObjectType):
    create_guide = CreateGuide.Field()
    update_guide = UpdateGuide.Field()
    delete_guide = DeleteGuide.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)