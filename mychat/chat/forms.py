from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    """
    Форма для регистрации пользователей.
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model() 
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")  # Include email, first_name and last_name fields


class LoginForm(AuthenticationForm):
    """
    Форма для входа пользователей.
    """
    pass