from django import forms


class PermitStatusForm(forms.Form):
    permit_id = forms.CharField(required=True,
                                label="Permit ID",
                                help_text="Enter your Permit Application ID")
