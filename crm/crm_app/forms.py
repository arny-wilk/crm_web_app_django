from typing import Tuple, Type

from django.contrib.auth.forms import UserCreationForm

from crm_app.models import UserManagementSystem


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model: Type[UserManagementSystem] = UserManagementSystem
        fields: tuple[str] = ("email", )
