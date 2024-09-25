from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    client_group, created = Group.objects.get_or_create(name='Client')
    admin_group, created = Group.objects.get_or_create(name='Admin')
    expert_group, created = Group.objects.get_or_create(name='Expert')

    user_content_type = ContentType.objects.get_for_model(User)
    admin_permissions = Permission.objects.filter(content_type=user_content_type)
    admin_group.permissions.set(admin_permissions)