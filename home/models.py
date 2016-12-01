from django.db import models
from biz_content.models import Category, StepPage

from wagtail.wagtailcore.models import Page


class HomePage(Page):

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['categories'] = Category.objects.all()
        context['step_pages'] = StepPage.objects.all()

        return context
