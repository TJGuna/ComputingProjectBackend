from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def create_groups(apps, schema_editor):
    client_group, created = Group.objects.get_or_create(name='Client')
    admin_group, created = Group.objects.get_or_create(name='Admin')
    expert_group, created = Group.objects.get_or_create(name='Expert')

    user_content_type = ContentType.objects.get_for_model(User)
    admin_permissions = Permission.objects.filter(content_type=user_content_type)
    admin_group.permissions.set(admin_permissions)

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # Adjust this to your actual auth app migration
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]