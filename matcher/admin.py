from django.contrib import admin
from wealthmap import models as wm_models
from wealthmap import admin as wm_admin
from . import forms


@admin.register(wm_models.get_search_model())
class OpportunityAdmin(wm_admin.AddCreator):
    form = forms.SearchModelForm
    list_display = ('title', 'agency', 'updated_at')
