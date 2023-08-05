from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

import graphene
from graphene_django import DjangoObjectType
from graphene_django_cud.mutations import DjangoBatchPatchMutation, DjangoCreateMutation
from guardian.shortcuts import get_objects_for_user

from aleksis.core.models import Activity
from aleksis.core.schema.base import (
    DeleteMutation,
    DjangoFilterMixin,
    FilterOrderList,
    PermissionBatchPatchMixin,
    PermissionsTypeMixin,
)
from aleksis.core.util.core_helpers import get_site_preferences, has_person
from aleksis.core.util.email import send_email

from .models import MailAddress, MailDomain


class MailAddressType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = MailAddress
        filter_fields = {"domain": ["in"]}


class MailDomainType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = MailDomain
        filter_fields = ("is_public",)


class MailAddressCreateMutation(DjangoCreateMutation):
    class Meta:
        model = MailAddress
        permissions = ("postbuero.create_mailaddress",)

    @classmethod
    def before_save(cls, root, info, input, obj):  # noqa
        obj.person = info.context.user.person
        return obj

    @classmethod
    def check_permissions(cls, root, info, input):  # noqa
        domain = MailDomain.get(id=input.domain)
        if info.context.user.has_perm("postbuero.can_use_domain_rule", domain):
            return
        raise PermissionDenied()

    @classmethod
    def validate_local_part(cls, root, info, value, input, **kwargs):  # noqa
        if value in get_site_preferences()["postbuero__disallowed_local_parts"].split(","):
            raise ValueError(_("Local part name is disallowed"))

    @classmethod
    def after_mutate(cls, root, info, input, obj, return_data):  # noqa
        recipient_list = [return_data["mail_address"], info.context.user.person.email]
        mail_context = {}
        mail_context["person"] = info.context.user.person

        if get_site_preferences()["postbuero__confirmation_mail"]:
            mail_context["address"] = return_data["mail_address"]
            if get_site_preferences()["postbuero__admin_mail"]:
                for admin in settings.ADMINS:
                    recipient_list.append(admin[1])
            # Send mail to user and admins
            send_email(
                template_name="mail_added",
                recipient_list=recipient_list,
                context=mail_context,
            )

        # Create activity
        act = Activity(
            title=_("You have added an email address"),
            description=_(
                f"You have added the email address {return_data['mail_address']} to your profile."
            ),
            app="Postbuero",
            user=mail_context["person"],
        )
        act.save()


class MailDomainCreateMutation(DjangoCreateMutation):
    class Meta:
        model = MailDomain
        permissions = ("postbuero.create_maildomain",)


class MailDomainDeleteMutation(DeleteMutation):
    klass = MailDomain
    permission_required = "postbuero.delete_maildomain"


class MailDomainBatchPatchMutation(PermissionBatchPatchMixin, DjangoBatchPatchMutation):
    class Meta:
        model = MailDomain
        permissions = "postbuero.change_maildomain"


class Query(graphene.ObjectType):
    mail_addresses_for_user = FilterOrderList(MailAddressType)

    mail_domains_for_user = graphene.List(MailDomainType)
    editable_mail_domains_for_user = FilterOrderList(MailDomainType)
    public_mail_domains = graphene.List(MailDomainType)

    disallowed_local_parts = graphene.List(graphene.String)

    @staticmethod
    def resolve_mail_addresses_for_user(root, info, **kwargs):
        if has_person(info.context):
            mail_addresses = info.context.user.person.local_mail_addresses.all()
            return mail_addresses
        return []

    @staticmethod
    def resolve_mail_domains_for_user(root, info, **kwargs):
        mail_domains = get_objects_for_user(
            info.context.user, "postbuero.can_use_domain", MailDomain.objects.all()
        ).union(MailDomain.objects.filter(is_public=True))
        return mail_domains

    @staticmethod
    def resolve_editable_mail_domains_for_user(root, info, **kwargs):
        mail_domains = get_objects_for_user(
            info.context.user, "postbuero.change_maildomain", MailDomain.objects.all()
        )
        return mail_domains

    @staticmethod
    def resolve_public_mail_domains(root, info, **kwargs):
        mail_domains = MailDomain.objects.filter(is_public=True)
        return mail_domains

    @staticmethod
    def resolve_disallowed_local_parts(root, info, **kwargs):
        return get_site_preferences()["postbuero__disallowed_local_parts"].split(",")


class Mutation(graphene.ObjectType):
    create_mail_address = MailAddressCreateMutation.Field()

    create_mail_domain = MailDomainCreateMutation.Field()
    delete_mail_domain = MailDomainDeleteMutation.Field()
    batch_patch_mail_domain = MailDomainBatchPatchMutation.Field()
