from django.db import models
from django.utils.translation import gettext_lazy as _

from aleksis.core.mixins import ExtensibleModel, ExtensiblePolymorphicModel
from aleksis.core.models import Group, Person


class MailDomain(ExtensibleModel):
    SCOPE_PREFIX_WEBMILTER = "maildomain"

    domain = models.CharField(verbose_name=_("Domain"), max_length=255)

    is_public = models.BooleanField(verbose_name=_("Public usable"), default=True)

    def __str__(self) -> str:
        return self.domain

    @property
    def scope_webmilter(self) -> str:
        """Return OAuth2 scope name to use WebMilter API."""
        return f"{self.SCOPE_PREFIX_WEBMILTER}_{self.domain}"

    class Meta:
        permissions = (("can_use_domain", _("Can use domain")),)


class MailAddress(ExtensibleModel):
    domain = models.ForeignKey(MailDomain, verbose_name=_("Domain"), on_delete=models.CASCADE)
    local_part = models.CharField(verbose_name=_("Local part"), max_length=64)
    person = models.ForeignKey(
        Person,
        verbose_name=_("Person"),
        null=True,
        on_delete=models.SET_NULL,
        related_name="local_mail_addresses",
    )

    def __str__(self) -> str:
        return f"{self.local_part}@{self.domain}"

    class Meta:
        verbose_name = _("Mail address")
        verbose_name_plural = _("Mail addresses")
        constraints = [
            models.UniqueConstraint(
                fields=["local_part", "domain"], name="unique_local_part_per_domain"
            )
        ]


class MailAlias(ExtensiblePolymorphicModel):
    domain = models.ForeignKey(MailDomain, verbose_name=_("Domain"), on_delete=models.CASCADE)
    local_part = models.CharField(verbose_name=_("Local part"), max_length=64)

    def __str__(self) -> str:
        return f"{self.local_part}@{self.domain}"

    def resolve(self, **kwargs):
        raise NotImplementedError("You must use the concrete model to resovle the alias.")

    class Meta:
        verbose_name = _("Mail alias")
        verbose_name_plural = _("Mail alias")
        constraints = [
            models.UniqueConstraint(fields=["local_part", "domain"], name="unique_alias_per_domain")
        ]


class MailAliasForPerson(MailAlias):
    person = models.ForeignKey(
        Person,
        verbose_name=_("Person"),
        null=True,
        on_delete=models.SET_NULL,
        related_name="local_mail_aliases",
    )

    def resolve(self, guardians: bool = False, **kwargs):
        """Resolve alias to the e-mail address of this person or its guardians."""
        if not self.person:
            return []

        if guardians:
            return list(self.person.guardians.all().values_list("email", flat=True))

        return [self.person.email]

    class Meta:
        verbose_name = _("Mail alias for a person")
        verbose_name_plural = _("Mail aliases for persons")


class MailAliasForGroup(MailAlias):
    group = models.ForeignKey(
        Group,
        verbose_name=_("Group"),
        null=True,
        on_delete=models.SET_NULL,
        related_name="local_mail_aliases",
    )

    def resolve(self, guardians: bool = False, owners: bool = False, **kwargs):
        """Resolve alias to the addresses of this group's members, owners, or their guardians."""
        if not self.group:
            return []

        if owners:
            pq = self.group.owners.all()
        else:
            pq = self.group.members.all()

        if guardians:
            pq = Person.objects.filter(children__in=pq)

        return list(pq.values_list("email", flat=True))

    class Meta:
        verbose_name = _("Mail alias for a group")
        verbose_name_plural = _("Mail aliases for groups")
