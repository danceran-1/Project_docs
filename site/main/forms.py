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
        

class RegistrationForm_true(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Пароль"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Подтвердите пароль"
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')
        labels = {
            'username': 'Логин',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        
        return cleaned_data

class CriterionForm(forms.ModelForm):
    class Meta:
        model = Criterion
        fields = ['name', 'file']

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")