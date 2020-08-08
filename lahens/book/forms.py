from django.forms import ModelForm
from .models import Pathtk, City, State, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class PathForm(forms.ModelForm):
    class Meta:
        model = Pathtk
        fields = '__all__'
        exclude = ['bus', 'pref_no']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_name'].queryset = City.objects.none()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']