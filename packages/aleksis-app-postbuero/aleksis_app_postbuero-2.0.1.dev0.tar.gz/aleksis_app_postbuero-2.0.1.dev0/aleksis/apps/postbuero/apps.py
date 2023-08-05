from django.apps import apps
from django.db import models
from django.db.models import functions
from django.utils.translation import gettext_lazy as _

from aleksis.core.util.apps import AppConfig


class PostBueroConfig(AppConfig):
    name = "aleksis.apps.postbuero"
    verbose_name = "AlekSIS — Postbuero (Mail server management)"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/Onboarding/AlekSIS-App-Postbuero",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2021], "Jonathan Weth", "dev@jonathanweth.de"),
        ([2021], "Tom Teichler", "tom.teichler@teckids.org"),
        ([2022], "Dominik George", "dominik.george@teckids.org"),
    )

    @classmethod
    def get_all_scopes(cls) -> dict[str, str]:
        """Return all OAuth scopes and their descriptions for this app."""
        MailDomain = apps.get_model("postbuero", "MailDomain")
        scopes = {}

        label_prefix_webmilter = _("Use WebMilter APIs for domain")
        scopes_webmilter = dict(
            MailDomain.objects.annotate(
                scope=functions.Concat(
                    models.Value(f"{MailDomain.SCOPE_PREFIX_WEBMILTER}_"),
                    models.F("domain"),
                    output_field=models.CharField(),
                ),
                label=functions.Concat(
                    models.Value(f"{label_prefix_webmilter}: "), models.F("domain")
                ),
            )
            .values_list("scope", "label")
            .distinct()
        )
        scopes.update(scopes_webmilter)

        return scopes
