from django.db import models
from biz_content.models import Category, StepPage

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class HomePage(Page):

    header_img = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_img'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['categories'] = Category.objects.all()
        context['step_pages'] = StepPage.objects.all()

        return context
