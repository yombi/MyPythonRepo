from django import forms

from applications.medicines.models import Medicine


class MedicineForm(forms.ModelForm):

    class Meta:
        model = Medicine
        fields = '__all__'
