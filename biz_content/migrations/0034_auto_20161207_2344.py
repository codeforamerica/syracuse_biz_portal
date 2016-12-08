from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('biz_content', '0033_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistitem',
            name='checklist',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklist_items', to='biz_content.StepPage'),
        ),
    ]