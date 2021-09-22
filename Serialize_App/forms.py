
from django import forms

from Serialize_App.models import Employee

class EmployeeModelForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'