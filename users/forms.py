from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
            "company_name",
            "company_domain",
            "company_city",
            "company_contact",
            "legal_document",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company_name"].required = False
        self.fields["company_domain"].required = False
        self.fields["company_city"].required = False
        self.fields["company_contact"].required = False
        self.fields["legal_document"].required = False
        self.fields["role"].required = True
        self.fields["email"].required = True
