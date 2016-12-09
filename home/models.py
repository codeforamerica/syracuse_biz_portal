from django.db import models
from biz_content.models import Category, CollectionPage, StepPage
from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.wagtailcore.models import Page, Orderable


class SelectablePages(models.Model):
    step_pages = models.ForeignKey(
        'biz_content.StepPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        PageChooserPanel('step_pages', 'biz_content.StepPage'),
    ]

    class Meta:
        abstract = True


class HomePageSelectedPages(Orderable, SelectablePages):
    page = ParentalKey(
        'home.HomePage',
        related_name='selected_pages',
        on_delete=models.SET_NULL, null=True)


class HomePage(Page):

    content_panels = Page.content_panels + [
        InlinePanel('selected_pages', label="Selected Pages"),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['categories'] = Category.objects.all()
        context['collection_pages'] = CollectionPage.objects.all()
        context['step_pages'] = StepPage.objects.all()

        return context
