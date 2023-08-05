from django.contrib.auth.models import User

from rules import predicate

from ..models import MailAddress, MailDomain


@predicate
def is_domain_public(user: User, domain: MailDomain) -> bool:
    """Check if domain is publicly usable."""
    return domain.is_public


@predicate
def is_mail_address_owner(user: User, address: MailAddress) -> bool:
    """Check if mail address is owned by the user's person."""
    return user.person == address.person
