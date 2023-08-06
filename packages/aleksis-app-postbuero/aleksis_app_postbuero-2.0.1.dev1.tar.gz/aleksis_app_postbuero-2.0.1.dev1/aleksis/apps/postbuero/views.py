from django.core.exceptions import BadRequest

from oauth2_provider.views.mixins import ScopedResourceMixin
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from aleksis.core.util.auth_helpers import ClientProtectedResourceMixin

from .models import MailAlias, MailDomain


class WebMilterDomainMixin(ScopedResourceMixin, ClientProtectedResourceMixin):
    """Base view for WebMilter domain operations."""

    def _get_address_parts(self):
        if "local" in self.kwargs:
            local_part, domain = self.kwargs["local"], self.kwargs["domain"]
        elif "address" in self.kwargs:
            if "@" not in self.kwargs["address"]:
                raise BadRequest(f"E-mail address {self.kwargs['address']} is malformed")
            local_part, domain = self.kwargs["address"].split("@")

        return local_part, domain

    def _get_domain(self):
        """Get domain object by either address or domain only."""
        local_part, domain = self._get_address_parts()

        return MailDomain.objects.get(domain=domain)

    def get_scopes(self, *args, **kwargs) -> list[str]:
        """Return the scope needed to access the domain."""
        return [self._get_domain().scope_webmilter]


class WebMilterAliasView(WebMilterDomainMixin, RetrieveAPIView):
    """View to resolve an alias address using WebMilter."""

    def get_object(self):
        local_part, domain = self._get_address_parts()
        local_part = local_part.split("+")[0]

        return MailAlias.objects.get(domain__domain=domain, local_part=local_part)

    def _resolve_args_from_local_part(self):
        local_part, domain = self._get_address_parts()

        args = {}

        if "+" not in local_part:
            return args

        extension = local_part.split("+")[1]
        mods = list(extension)
        if "g" in mods:
            args["guardians"] = True
        if "o" in mods:
            args["owners"] = True

        return args

    def retrieve(self, request, *args, **kwargs):
        args = self._resolve_args_from_local_part()
        return Response(self.get_object().resolve(**args))
