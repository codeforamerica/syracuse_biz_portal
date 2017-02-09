import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

NO_CU_ERROR = "Your business license identifier must start with CU"

INVALID_CHARACTER_ERROR = ("Your identifier must only contain "
                           "numbers and letters.")


class PermitStatusForm(forms.Form):
    permit_id = forms.CharField(required=True,
                                label="Permit ID",
                                help_text="Enter your Permit Application ID")


def starts_with_cu(value):
    if not value.startswith('CU'):
        raise forms.ValidationError(NO_CU_ERROR)


def is_letter_number_dashes(value):
    type_validation = re.match(r'[A-Za-z0-9-]*$', value)
    if not type_validation:
        raise forms.ValidationError(INVALID_CHARACTER_ERROR)


class BizLicenseStatusForm(forms.Form):
    cu_id = forms.CharField(required=True,
                            label="Certificate of Use ID",
                            help_text="Example: CU2000-1234",
                            validators=[starts_with_cu,
                                        is_letter_number_dashes])
