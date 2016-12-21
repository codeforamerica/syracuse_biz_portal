from django.db import migrations, models

def add_projects(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model("auth", "User")
    Project = apps.get_model("biz_content", "Project")
    user_with_projects = Project.objects.values('owner')
    for user in User.objects.exclude(pk__in=user_with_projects):
        Project.objects.create(owner=user)

class Migration(migrations.Migration):

    dependencies = [
        ('biz_content', '0041_auto_20161221_0001'),
    ]

    operations = [
        migrations.RunPython(add_projects)
    ]
