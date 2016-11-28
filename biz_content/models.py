from __future__ import unicode_literals

from django.db import models
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, PageChooserPanel
from modelcluster.fields import ParentalKey  # Installed with Wagtail, ModelCluster provides many custom field-types that Wagtail relies on
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel



# Create your models here.


############################################################################
"""
CATEGORIES & CHECKLISTS
"""
class Category(models.Model):
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

    category = models.ForeignKey(Category, related_name="checklists", null=True, blank=True)

    items = StreamField([
        ('text', blocks.CharBlock(max_length=255,
                                  null=True,
                                  classname="text",
                                  label="Checklist Text",
                                  help_text="Add a Checklist Item"
                                  )),
        ], null=True)

    def __unicode__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('category'),
        StreamFieldPanel('items')
    ]


        # add function here to create step page with slug that matches a checklist
        # if checklist is deleted, make sure the page deletes too!



class ChecklistItem(models.Model):
    """
    Represents an item in a checklist.
    """
    checklist = ParentalKey('Checklist', related_name='checklist_items', null=True)

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
register_snippet(Checklist)

###################################

# title is inherited from the Page model!
class StepPage(Page):
    date = models.DateTimeField("Post date")
    description = models.CharField(max_length=2000,null=True)
    category = models.ForeignKey(Category, related_name="step_pages", null=True, blank=True,on_delete=models.SET_NULL )

    header_img = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    checklist = models.ForeignKey(
    'biz_content.Checklist',
    null=True,
    blank=True,
    on_delete=models.PROTECT,
    related_name='+'
    )

    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text='Choose an existing page if you want the link to point somewhere inside the CMS.'
    )

    # search_fields = Page.search_fields + (
    #     index.SearchField('intro'),
    # )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('description'),
        ImageChooserPanel('header_img'),
        SnippetChooserPanel('checklist'),
        FieldPanel('link_page'),
        FieldPanel('category'),
        InlinePanel('content_paragraph', label="Paragraph Section")
    ]

class ContentParagraph(models.Model):
    page = ParentalKey('biz_content.StepPage', related_name='content_paragraph', null=True)
    header = models.CharField(
        max_length=1000,null=True
    )
    subheader = models.CharField(
        max_length=1000,null=True
    )
    body = RichTextField(blank=True)

    resources = StreamField([
        ('phone_number', blocks.IntegerBlock(max_length=255,
                                  null=True,
                                  classname="phone_number",
                                  label="Phone Number",
                                  help_text="Add a Phone Number"
                                  )),
        ('email', blocks.EmailBlock(null=True,
                                  classname="email",
                                  label="Email",
                                  help_text="Add an email"
                                  )),
        ('link', blocks.CharBlock(max_length=1000,
                                  null=True,
                                  classname="text",
                                  label="Resource Link",
                                  help_text="Add resource link"
                                  )),
    ], null=True)

    panels = [
        FieldPanel('header'),
        FieldPanel('subheader'),
        FieldPanel('body'),
        StreamFieldPanel('resources')
    ]

