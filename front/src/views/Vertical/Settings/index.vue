<script setup lang="ts">
import Setting from "@/layouts/Setting/index.vue";
import SettingAction from "@/layouts/Setting/SettingAction.vue";
import SettingActionDropdown from "@/layouts/Setting/SettingActionDropdown.vue";

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
</script>

<template>
  <setting>
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
      <setting-action :title="'System'" :path="'/settings/system'">
        <icon-ant-design-setting-filled class="views-setting-action-icon" style="font-size: 1.4rem" />
      </setting-action>
    </div>
  </setting>
</template>
