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
      :gql-patch-mutation="gqlPatchMutation"
      :gql-delete-mutation="gqlDeleteMutation"
      :default-item="defaultItem"
      :get-create-data="mailDomainCreateData"
      :get-patch-data="mailDomainPatchData"
      create-item-i18n-key="postbuero.mail_domains.create"
      filter
    >
      <template #domain.field="{ attrs, on }">
        <v-text-field
          v-bind="attrs"
          v-on="on"
          :rules="domainRule"
        />
      </template>
      
      <template #isPublic="{ item }">
        <v-icon>{{ "mdi-" }}{{ item.isPublic ? "check" : "close" }}</v-icon>
      </template>

      <template #isPublic.field="{ attrs, on }">
        <v-checkbox
          v-bind="attrs"
          v-on="on"
        />
      </template>

      <template #filters="{ attrs, on }">
        <v-select
          v-bind="attrs('is_public')"
          v-on="on('is_public')"
          :label="$t('postbuero.mail_domains.data_table.is_public')"
          :items="publicFilterSelectItems"
          item-text="text"
          item-value="value"
        />
      </template>
    </inline-c-r-u-d-list>
  </div>
</template>

<script>
import { editableMailDomainsForUser, createMailDomain, deleteMailDomain, patchMailDomain } from "./mailDomains.graphql";

export default {
  name: "MailDomainCRUDList",
  data() {
    return {
      headers: [
        { text: this.$t("postbuero.mail_domains.data_table.domain"), value: "domain" },
        { text: this.$t("postbuero.mail_domains.data_table.is_public"), value: "isPublic" },
      ],
      i18nKey: "postbuero.mail_domains",
      gqlQuery: editableMailDomainsForUser,
      gqlCreateMutation: createMailDomain,
      gqlDeleteMutation: deleteMailDomain,
      gqlPatchMutation: patchMailDomain,
      defaultItem: {
        domain: "",
        isPublic: true,
      },
      publicFilterSelectItems: [
        {text: this.$t("postbuero.mail_domains.data_table.filters.show_all"), value: null},
        {text: this.$t("postbuero.mail_domains.data_table.filters.only_public"), value: true},
        {text: this.$t("postbuero.mail_domains.data_table.filters.only_non_public"), value: false},
      ],
    }
  },
  computed: {
    requiredRule() {
      return [v => !!v || this.$t("forms.errors.required"),];
    },
    domainRule() {
      return [v => /(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]/.test(v) || this.$t("postbuero.mail_domains.data_table.errors.domain_invalid"),];
    },
  },
  methods: {
    mailDomainCreateData(item) {
      return {
        domain: item.domain,
        isPublic: !!item.isPublic,
      };
    },
    mailDomainPatchData(items) {
      return items.map(
        (item) => ({
          id: item.id,
          domain: item.domain,
          isPublic: !!item.isPublic,
        })
      );
    },
  },
}
</script>

<style scoped>

</style>
