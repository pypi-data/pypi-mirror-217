from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import BooleanPreference, LongStringPreference

from aleksis.core.registries import site_preferences_registry

postbuero = Section("postbuero", verbose_name=_("Postbuero"))


@site_preferences_registry.register
class DisallowedLocalParts(LongStringPreference):
    section = postbuero
    name = "disallowed_local_parts"
    required = False
    default = (
        "bin,daemon,Debian-exim,freerad,games,gnats,irc,list,lp,mail,man,messagebus,news,"
        "nslcd,ntp,openldap,postfix,postgres,proxy,root,sshd,sssd,statd,sync,sys,systemd-bus-proxy,"
        "systemd-network,systemd-resolve,systemd-timesync,uucp,www-data,"
        "webmaster,hostmaster,postmaster"
    )
    verbose_name = _("Comma-seperated list of disallowed local parts")


@site_preferences_registry.register
class SendMail(BooleanPreference):
    section = postbuero
    name = "confirmation_mail"
    required = False
    default = True
    verbose_name = _(
        "Sent notification to user and new address if a new email address was registered."
    )


@site_preferences_registry.register
class SendAdminMail(BooleanPreference):
    section = postbuero
    name = "admin_mail"
    required = False
    default = False
    verbose_name = _("Sent notification to admins if a new email address was registered.")
