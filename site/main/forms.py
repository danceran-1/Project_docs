from django import forms
from .models import User
from .models import Criterion

class RegistrationForm(forms.ModelForm):
    """Это авторизация"""
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        



class CriterionForm(forms.ModelForm):
    class Meta:
        model = Criterion
        fields = ['name', 'file']

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")