from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, PageChooserPanel
from modelcluster.fields import ParentalKey  # Installed with Wagtail, ModelCluster provides many custom field-types that Wagtail relies on
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks



# Create your models here.


class Category(ClusterableModel):
    """
    Represents a category for business development.
    """
    page = models.ForeignKey( # what page do we want to display this poll on?
        'wagtailcore.Page',
        related_name='categories',
        null=True,
        blank=True
    )

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
        FieldPanel('slug'),
        InlinePanel('checklist', label="Checklist")
    ]

class Checklist(models.Model):
    """
    Represents a checklist for a given Category.
    """
    page = ParentalKey('biz_content.Category', related_name='checklist', null=True)


    name = models.CharField(
        max_length=255,null=True
    )
    description = models.CharField(
        max_length=3000,null=True
    )
    slug = models.CharField(
        max_length=255,null=True
    )
    category = models.ForeignKey(Category, related_name="checklists", null=True)

    items = StreamField([
        ('text', blocks.CharBlock(max_length=255,null=True, classname="text", label="Checklist Text")),
    ], null=True)

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('slug'),
        StreamFieldPanel('items')
    ]



class ChecklistItem(models.Model):
    """
    Represents an item in a checklist.
    """
    # checklist = ParentalKey('Checklist', related_name='checklist_items', null=True)

    text = models.CharField(
        max_length=255,null=True
    )
    completed = models.BooleanField(default=False)
    order_num = models.IntegerField(default=0)
    checklist = models.ForeignKey(Checklist,
        related_name='checklist_items', null=True)

    def __unicode__(self):
        return self.text


register_snippet(Category)
register_snippet(Category)

