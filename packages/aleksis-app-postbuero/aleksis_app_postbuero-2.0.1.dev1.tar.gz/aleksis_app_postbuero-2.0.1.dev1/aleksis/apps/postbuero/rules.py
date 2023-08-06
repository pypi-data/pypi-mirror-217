import rules

from aleksis.core.util.predicates import has_global_perm, has_object_perm, has_person

from .util.predicates import is_domain_public, is_mail_address_owner

edit_mail_address_predicate = has_person & (
    is_mail_address_owner | has_global_perm("postbuero.change_mailaddress")
)
rules.add_perm("postbuero.edit_mailaddress_rule", edit_mail_address_predicate)

can_use_domain_predicate = has_person & (
    is_domain_public | has_object_perm("postbuero.can_use_domain")
)
rules.add_perm("postbuero.can_use_domain_rule", can_use_domain_predicate)

view_mail_domain_predicate = has_person & has_global_perm("postbuero.view_maildomain")
rules.add_perm("postbuero.view_maildomain_rule", view_mail_domain_predicate)

create_mail_domain_predicate = has_person & has_global_perm("postbuero.add_maildomain")
rules.add_perm("postbuero.create_maildomain_rule", create_mail_domain_predicate)

edit_mail_domain_predicate = has_person & has_global_perm("postbuero.change_maildomain")
rules.add_perm("postbuero.edit_maildomain_rule", edit_mail_domain_predicate)
