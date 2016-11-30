# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-30 02:57
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('biz_content', '0024_auto_20161129_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentparagraph',
            name='page',
        ),
        migrations.AddField(
            model_name='steppage',
            name='page_content',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title', icon='title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('email', wagtail.wagtailcore.blocks.EmailBlock(classname='email', help_text='Add an email', label='Email', null=True)), ('phone_number', wagtail.wagtailcore.blocks.IntegerBlock(classname='phone_number', help_text='Add a Phone Number', label='Phone Number', max_length=255, null=True)), ('link', wagtail.wagtailcore.blocks.URLBlock(classname='text', help_text='Add resource link', label='Resource Link', max_length=1000, null=True))), blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='ContentParagraph',
        ),
    ]
