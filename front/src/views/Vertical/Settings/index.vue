<template>
  <div class="flex flex-col w-2/3 mx-auto mt-4">
    <div class="flex"></div>
    <div class="flex flex-row">
      <div class="flex flex-col w-1/6 divide-y divide-gray-500">
        <div class="views-setting-actions">
          <setting-action :title="'Account'" :path="'/settings/account'">
            <icon-ic-baseline-person class="views-setting-action-icon" style="font-size: 1.4rem" />
          </setting-action>
          <setting-action :title="'Appearance'" :path="'/settings/appearance'">
            <icon-ic-outline-edit class="views-setting-action-icon" style="font-size: 1.4rem" />
          </setting-action>
          <setting-action :title="'Authentication'" :path="'/settings/authentication'">
            <icon-ic-baseline-security class="views-setting-action-icon" style="font-size: 1.4rem" />
          </setting-action>
        </div>
        <div class="views-setting-actions">
          <span class="views-setting-action-category">Search</span>
          <setting-action-dropdown :title="'Tag'" :options="tagOptions">
            <template v-slot:icon>
              <icon-ion-ios-pricetags class="views-setting-action-icon" style="font-size: 1.4rem" />
            </template>
          </setting-action-dropdown>
          <setting-action-dropdown :title="'Elasticsearch'" :options="elasticsearchQueryOptions">
            <template v-slot:icon>
              <icon-ic-baseline-search class="views-setting-action-icon" style="font-size: 1.4rem" />
            </template>
          </setting-action-dropdown>
          <setting-action-dropdown :title="'Quest'" :options="questOptions">
            <template v-slot:icon>
              <icon-icons8-todo-list class="views-setting-action-icon" style="font-size: 1.4rem" />
            </template>
          </setting-action-dropdown>
        </div>
        <div class="views-setting-actions">
          <span class="views-setting-action-category">Administration</span>
          <setting-action :title="'Users'" :path="'/settings/users'">
            <icon-ic-baseline-group class="views-setting-action-icon" style="font-size: 1.4rem" />
          </setting-action>
          <setting-action :title="'Group'" :path="'/settings/group'">
            <icon-fa-group class="views-setting-action-icon" style="font-size: 1.4rem" />
          </setting-action>
          <setting-action-dropdown :title="'Storage'" :options="storageOptions">
            <template v-slot:icon>
              <icon-mdi-storage class="views-setting-action-icon" style="font-size: 1.4rem" />
            </template>
          </setting-action-dropdown>
        </div>
      </div>
      <div class="flex w-full">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import RippleButton from "@/elements/Button/RippleButton.vue";

import SettingAction from "./SettingAction.vue";
import SettingActionDropdown from "./SettingActionDropdown.vue";

export default {
  components: { RippleButton, SettingAction, SettingActionDropdown },
  setup() {
    const tagOptions = [
      { title: "Tag", path: "/settings/tag" },
      { title: "Token", path: "/settings/tag-token" },
      { title: "Attribute", path: "/settings/tag-attribute" },
      { title: "Front UI", path: "/settings/tag-front-ui" },
    ];

    const elasticsearchQueryOptions = [
      { title: "Count", path: "/settings/elasticsearch-count" },
      { title: "Search", path: "/settings/elasticsearch-search" },
    ];
    const questOptions = [
      { title: "Quest", path: "/settings/quest" },
      { title: "Elastic Count Quest", path: "/settings/elasticsearch-count-quest" },
    ];
    const storageOptions = [{ title: "MinIO", path: "/settings/storage-minio" }];

    return { tagOptions, elasticsearchQueryOptions, questOptions, storageOptions };
  },
};
</script>
