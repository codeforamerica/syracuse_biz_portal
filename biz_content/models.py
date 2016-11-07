from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel

# Create your models here.


class Category(models.Model):
    """
    Represents a category for business development.
    """
    name = models.CharField(
        max_length=255,null=True
    )
    slug = models.CharField(
        max_length=255,null=True
    )

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

class Checklist(models.Model):
    """
    Represents a checklist for a given Category.
    """
    name = models.CharField(
        max_length=255,null=True
    )
    description = models.CharField(
        max_length=3000,null=True
    )
    slug = models.CharField(
        max_length=255,null=True
    )
    category = models.ForeignKey(Category,
        related_name='checklist', null=True)

    def __unicode__(self):
        return self.name

class ChecklistItem(models.Model):
    """
    Represents an item in a checklist.
    """
    text = models.CharField(
        max_length=255,null=True
    )
    completed = models.BooleanField(default=False)
    order_num = models.IntegerField(default=0)
    checklist = models.ForeignKey(Checklist,
        related_name='options', null=True)

    def __unicode__(self):
        return self.text


register_snippet(Category)
