from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from material import Layout, Row

from aleksis.core.mixins import ExtensibleForm
from aleksis.core.util.core_helpers import get_site_preferences

from .models import MailAddress, MailDomain

User = get_user_model()


class MailAddForm(ExtensibleForm):
    layout = Layout(
        Row("local_part", "domain"),
    )

    class Meta:
        model = MailAddress
        exclude = ["person"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["domain"].queryset = MailDomain.objects.filter(is_public=True)

    def clean_local_part(self):
        local_part = self.cleaned_data["local_part"]

        disallowed_local_parts = get_site_preferences()["postbuero__disallowed_local_parts"].split(
            ","
        )

        if local_part in disallowed_local_parts:
            raise forms.ValidationError(_("Local part not allowed."))

        address = f"{self.cleaned_data['local_part']}@{self.cleaned_data['domain']}"
        validate_email(address)

        return local_part

    def save(self, person, *args, **kwargs):
        self.instance.person = person

        super().save(*args, **kwargs)
