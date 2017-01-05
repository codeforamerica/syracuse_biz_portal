from django import forms
from .models import Project


class ProjectNotebookForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Project
        fields = [
            'ny_state_cert_of_auth_number',
            'additional_state_license_number',
            'business_license_number',
            'business_structure',
            'dba_name',
            'business_type',
            'number_of_employees',
            'street_address',
            'tax_address',
            'emergency_address',
            'zip_code',
            'parcel_number',
            'business_improvement_district',
            'square_footage',
            'number_parking_spaces',
        ]
