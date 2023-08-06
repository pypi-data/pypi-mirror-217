import {
  notLoggedInValidator,
  hasPersonValidator,
} from "aleksis.core/routeValidators";

export default {
  meta: {
    inMenu: true,
    titleKey: "postbuero.menu_title",
    icon: "mdi-email-multiple-outline",
    validators: [hasPersonValidator],
  },
  children: [
    {
      path: "mail_addresses/manage",
      component: () => import("./components/mail_addresses/MailAddressCRUDList.vue"),
      name: "postbuero.manageMailAddresses",
      meta: {
        inMenu: true,
        titleKey: "postbuero.mail_addresses.menu_title",
        icon: "mdi-at",
        validators: [hasPersonValidator],
      },
    },
    {
      path: "mail_domains/manage",
      component: () => import("./components/mail_domains/MailDomainCRUDList.vue"),
      name: "postbuero.manageMailDomains",
      meta: {
        inMenu: true,
        titleKey: "postbuero.mail_domains.title_plural",
        icon: "mdi-web",
        permission: "postbuero.view_maildomain",
      },
    },
  ],
};
