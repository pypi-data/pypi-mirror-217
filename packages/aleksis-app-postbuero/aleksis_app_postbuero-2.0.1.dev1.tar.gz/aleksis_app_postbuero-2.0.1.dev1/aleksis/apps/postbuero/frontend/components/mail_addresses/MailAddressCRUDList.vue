<script setup>
import InlineCRUDList from "aleksis.core/components/generic/InlineCRUDList.vue";
import DeleteDialog from "aleksis.core/components/generic/dialogs/DeleteDialog.vue";
</script>

<template>
  <div>
    <inline-c-r-u-d-list
      :headers="headers"
      :i18n-key="i18nKey"
      :gql-query="gqlQuery"
      :gql-create-mutation="gqlCreateMutation"
      :default-item="defaultItem"
      create-item-i18n-key="postbuero.mail_addresses.create"
      filter
    >
      <template #localPart.field="{ attrs, on }">
        <v-text-field
          v-bind="attrs"
          v-on="on"
          :rules="emailLocalPartRule"
        />
      </template>
      
      <template #domain="{ item }">
        {{ "@" + item.domain.domain }}
      </template>

      <template #domain.field="{ attrs, on }">
        <v-autocomplete
          v-bind="attrs"
          v-on="on"
          hide-no-data
          :items="mailDomains"
          item-text="domain"
          item-value="id"
          :loading="$apollo.queries.mailDomains.loading"
          :rules="requiredRule"
          prepend-icon="mdi-at"
        />
      </template>

      <template #filters="{ attrs, on }">
        <v-autocomplete
          v-bind="attrs('domain__in')"
          v-on="on('domain__in')"
          :label="$t('postbuero.mail_addresses.data_table.domain')"
          hide-no-data
          multiple
          :items="mailDomains"
          item-text="domain"
          item-value="id"
          :loading="$apollo.queries.mailDomains.loading"
        />
      </template>
    </inline-c-r-u-d-list>
  </div>
</template>

<script>
import { mailAddressesForUser, createMailAddress, mailDomainsForUser, disallowedLocalParts } from "./mailAddresses.graphql";

export default {
  name: "MailAddressCRUDList",
  data() {
    return {
      headers: [
        { text: this.$t("postbuero.mail_addresses.data_table.local_part"), value: "localPart" },
        { text: this.$t("postbuero.mail_addresses.data_table.domain"), value: "domain" },
      ],
      i18nKey: "postbuero.mail_addresses",
      gqlQuery: mailAddressesForUser,
      gqlCreateMutation: createMailAddress,
      defaultItem: {
        domain: "",
        localPart: "",
      },
    }
  },
  apollo: {
    mailDomains: mailDomainsForUser,
    disallowedLocalParts: disallowedLocalParts,
  },
  computed: {
    requiredRule() {
      return [v => !!v || this.$t("forms.errors.required"),];
    },
    emailLocalPartRule() {
      return [
        v => !!v || this.$t("forms.errors.required"),
        v => /^\w+([.!#$%&'*+-\/=?^_`{|}~]?\w+)*$/.test(v) || this.$t("postbuero.mail_addresses.data_table.errors.local_part_invalid_characters"),
        v => this.disallowedLocalParts.indexOf(v) === -1 || this.$t("postbuero.mail_addresses.data_table.errors.local_part_disallowed"),
      ];
    },
  },
}
</script>

<style scoped>

</style>
