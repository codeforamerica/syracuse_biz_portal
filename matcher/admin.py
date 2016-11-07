from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from wealthmap import models as wm_models
from wealthmap import admin as wm_admin
from . import forms


@admin.register(wm_models.get_search_model())
class OpportunityAdmin(wm_admin.AddCreator):
    form = forms.OpportunityForm
    list_display = ('title', 'agency', 'updated_at')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
