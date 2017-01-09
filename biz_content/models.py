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
from wagtail.wagtailcore.blocks import CharBlock, RichTextBlock, IntegerBlock
from wagtail.wagtailcore.blocks import URLBlock, EmailBlock
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from biz_content import forms


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

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('header_img'),
        StreamFieldPanel('page_content'),
        InlinePanel('checklist_items', label="Checklist Items"),
    ]

    def previous_step(self):
        if self.get_prev_sibling():
            return sefl.get_prev_sibling().url
        else:
            return self.get_siblings().last().url

    def next_step(self):
        if self.get_next_sibling():
            return self.get_next_sibling().url
        else:
            return self.get_siblings().first().url

    def get_context(self, request):
        context = super().get_context(request)
        projects = []
        checklists = []
        if request.user.is_authenticated():
            projects = request.user.projects.all()
        if projects:
            for project in projects:
                checklists.append(forms.ChecklistForm(self, project=project))
        else:
            checklists.append(forms.ChecklistForm(self))
        context['checklists'] = checklists
        return context


class ChecklistItem(Orderable):
    checklist = ParentalKey(StepPage, related_name='checklist_items')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Project(models.Model):
    name = models.CharField(max_length=255, default="New Project")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='projects')
    ny_state_cert_of_auth_number = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    additional_state_license_number = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    business_license_number = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    business_structure = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    dba_name = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True)
    number_of_employees = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    street_address = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    tax_address = models.CharField(max_length=255, blank=True, null=True)
    emergency_address = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    zip_code = models.CharField(
        max_length=255,
        blank=True, null=True)
    parcel_number = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    business_improvement_district = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    square_footage = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    number_parking_spaces = models.CharField(
        max_length=255,
        blank=True,
        null=True)

    checklists = models.ManyToManyField(StepPage)
    checked_items = models.ManyToManyField(ChecklistItem)

    def get_checklists(self):
        for checklist in self.checklists.all():
            yield forms.ChecklistForm(checklist, project=self)

    def __str__(self):
        return self.name


def create_users_first_project(sender, instance, created, **kwargs):
    if created:
        Project.objects.create(owner=instance)

post_save.connect(create_users_first_project, sender='auth.User')


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
