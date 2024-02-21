from django import forms

from apps.warehouse.models.warehouse import MaterialCutOutcome


class MaterialOutcomeForm(forms.ModelForm):
    class Meta:
        model = MaterialCutOutcome
        fields = ["cut", "is_ready"]

    def __init__(self, *args, **kwargs):
        super(MaterialOutcomeForm, self).__init__(*args, **kwargs)
        if self.fields:
            self.fields["cut"].queryset = self.fields["cut"].queryset.filter(
                is_ready=False
            )
