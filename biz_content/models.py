from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel, PageChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


class CustomCleanRegexBlock(blocks.RegexBlock):

    """
    Makes it easy to clean up Regex fields before saved.
    """

    def __init__(self, *args, **kwargs):
        self.custom_clean = kwargs.pop('custom_clean')
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        return self.custom_clean(value)


def clean_phone_number(value):
    return int("".join(_ for _ in value if _ in "1234567890"))


class PhoneBlock(blocks.StructBlock):
    phone_number = CustomCleanRegexBlock(
        regex=r'^\D*[2-9]\D*(\d\D*){9}$',
        custom_clean=clean_phone_number,
        error_messages={
            "invalid": "Add a ten digit phone number not starting with 1",
        },
        classname="phone_number",
        label="Phone Number (10 digits)",
        help_text="Add a 10 digit phone number, including area code")
    ext = blocks.IntegerBlock(
        required=False,
        min_value=1,
        classname="ext",
        label="Extension",
        help_text="Add optional extension")

    class Meta:
        icon = 'fa-phone'
        template = "biz_content/content_blocks/phone_block.html"


class ContentBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="full title", icon="title")
    paragraph = blocks.RichTextBlock()
    email = blocks.EmailBlock(
        classname="email",
        label="Email",
        help_text="Add an email",
        template="biz_content/content_blocks/email_block.html")
    phone_number = PhoneBlock(
        classname="phone_number",
        label="Phone Number",)
    link = blocks.StructBlock(
        [
            ('link_text', blocks.CharBlock()),
            ('link_url', blocks.URLBlock())
        ],
        classname="text",
        label="Link",
        help_text="Add resource link",
        icon="fa-link",
        template="biz_content/content_blocks/url_block.html")
    alert_text = blocks.CharBlock(
        max_length=2000,
        classname="alert_text",
        label="Alert Text",
        help_text="Add Alert Text",
        icon="fa-exclamation",
        template="biz_content/content_blocks/alert_text.html")
    embed_block = blocks.RawHTMLBlock(
        icon="fa-code",
        help_text="Copy and paste a map or video embed directly here.")


class CollectionPage(Page):

    """
    Represents a collection of step pages.
    """

    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    header_img = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = models.CharField(max_length=2000, null=True)
    page_content = StreamField(ContentBlock(), null=True, blank=True)

    start_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text=('Choose an existing page if you want the link ',
                   'to point somewhere inside the CMS.')
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('icon'),
        ImageChooserPanel('header_img'),
        StreamFieldPanel('page_content'),
        FieldPanel('start_link'),
    ]

    subpage_types = ['biz_content.StepPage']


class StepPage(Page):
    description = models.CharField(max_length=2000, null=True)
    page_content = StreamField(ContentBlock(), null=True, blank=True)
    header_img = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('header_img'),
        StreamFieldPanel('page_content'),
        InlinePanel('checklist_items', label="Checklist Items"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Determine previous and next step pages
        if self.get_prev_sibling():
            context['previous_step'] = self.get_prev_sibling().url
        else:
            context['previous_step'] = self.get_siblings().last().url

        if self.get_next_sibling():
            context['next_step'] = self.get_next_sibling().url
        else:
            context['next_step'] = self.get_siblings().first().url

        return context


class ChecklistItem(Orderable):
    checklist = ParentalKey(StepPage, related_name='checklist_items')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


@register_setting
class FooterSettings(BaseSetting):
    first_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text=('Choose a page to display in the 1st column of the footer')
    )
    second_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text=('Choose a page to display in the 2nd column of the footer')
    )
    third_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text=('Choose a page to display in the 3rd column of the footer')
    )
    department_name = models.CharField(
        max_length=255,
        help_text="The name of the department.",
        null=True)
    street_address = models.CharField(
        max_length=255,
        help_text="The department's street address, e.g. 1234 Main St.",
        null=True)
    city_state_zip = models.CharField(
        max_length=255,
        help_text="E.g. Syracuse, NY 13202.",
        null=True)
    phone = models.CharField(
        max_length=255,
        help_text="The departnment's phone number",
        null=True)


class StandAloneContentPage(Page):

    """
    Represents a stand alone content page.
    """

    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    header_img = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = models.CharField(max_length=2000, null=True)
    page_content = StreamField(ContentBlock(), null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('icon'),
        ImageChooserPanel('header_img'),
        StreamFieldPanel('page_content')
    ]
