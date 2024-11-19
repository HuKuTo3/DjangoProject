from django import forms
from django.contrib.auth.models import User

from testTask.models import Collection, Link


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url']

class LinkUpdateForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['title', 'description', 'image']