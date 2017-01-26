from django import forms


class PermitStatusForm(forms.Form):
    permit_id = forms.CharField(required=True,
                                label="Permit ID",
                                help_text="Enter your Permit Application ID")


class BizLicenseStatusForm(forms.Form):
    cu_id = forms.CharField(required=True,
                            label="Certificate of Use ID",
                            help_text="Enter your Certificate of Use ID")

    def clean_cu_id(self):
        cu_id = self.cleaned_data['cu_id']

        if "CU" not in cu_id:
            raise forms.ValidationError(
                "Your business license identifier must start with CU")
        return cu_id
