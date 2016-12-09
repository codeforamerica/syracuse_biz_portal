from django.db import models
from biz_content.models import Category, CollectionPage, StepPage

from wagtail.wagtailadmin.edit_handlers import InlinePanel, FieldPanel
from wagtail.wagtailcore.models import Page, Orderable


class SelectedPages(Orderable, StepPage):
    page = ParentalKey('biz_content.StepPage', related_name='selected_pages')


class HomePage(Page):

    content_panels = Page.content_panels + [
        InlinePanel('selected_pages'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['categories'] = Category.objects.all()
        context['collection_pages'] = CollectionPage.objects.all()
        context['step_pages'] = StepPage.objects.all()

        return context
