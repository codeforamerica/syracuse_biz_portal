from django.conf import settings
from django.db import models
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel, PageChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import CharBlock, RichTextBlock, IntegerBlock
from wagtail.wagtailcore.blocks import URLBlock, EmailBlock
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class Category(models.Model):
    """
    Represents a category for business development.
    """
    name = models.CharField(
        max_length=255, null=True
    )
    slug = models.CharField(
        max_length=255, null=True
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

register_snippet(Category)


class StepPage(Page):
    date = models.DateTimeField("Post date")
    description = models.CharField(max_length=2000, null=True)
    category = models.ForeignKey(
        Category,
        related_name="step_pages",
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    page_content = StreamField([
        ('heading', blocks.CharBlock(classname="full title", icon="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('email', blocks.EmailBlock(
                    null=True,
                    classname="email",
                    label="Email",
                    help_text="Add an email",
                    template="biz_content/content_blocks/email_block.html"
        )),
        ('phone_number', blocks.IntegerBlock(
                    max_length=255,
                    null=True,
                    classname="phone_number",
                    label="Phone Number",
                    help_text="Add a Phone Number",
                    template="biz_content/content_blocks/phone_block.html"
        )),
        ('alert_text', blocks.CharBlock(
                    max_length=2000,
                    null=True,
                    classname="alert_text",
                    label="Alert Text",
                    help_text="Add Alert Text",
                    template="biz_content/content_blocks/alert_text.html"
        )),
        ('link', blocks.StructBlock(
            [
                ('link_text', blocks.CharBlock()),
                ('link_url', blocks.URLBlock())
            ],
            null=True,
            classname="text",
            label="Resource Link",
            help_text="Add resource link",
            template="biz_content/content_blocks/url_block.html"
        ))
    ], null=True, blank=True)

    header_img = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text=('Choose an existing page if you want the link ',
                   'to point somewhere inside the CMS.')
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('description'),
        ImageChooserPanel('header_img'),
        StreamFieldPanel('page_content'),
        FieldPanel('link_page'),
        FieldPanel('category'),
        InlinePanel('checklist_items', label="Checklist Items"),
    ]


class ChecklistItem(Orderable):
    checklist = ParentalKey(StepPage, related_name='checklist_items')
    text = models.CharField(max_length=255)


class Project(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    checklists = models.ManyToManyField(StepPage)
    checked_items = models.ManyToManyField(ChecklistItem)
