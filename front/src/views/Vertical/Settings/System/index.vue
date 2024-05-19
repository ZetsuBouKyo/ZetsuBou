<script setup lang="ts">
import { watch } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownMode, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";
import { AppModeEnum, LoggingLevelEnum } from "@/interface/setting";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";

import { getOptionsFromEnum, initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { settingSystemState } from "@/state/Setting/system";

import { getTimezoneOptions } from "@/utils/timezone";

settingSystemState.init();

const appMode = initSelectDropdownState() as SelectDropdownState;
const appModeOptions = getOptionsFromEnum(AppModeEnum);

const timezone = initSelectDropdownState() as SelectDropdownState;
const timezoneOptions = getTimezoneOptions();

const loggingLevel = initSelectDropdownState() as SelectDropdownState;
const loggingLevelOptions = getOptionsFromEnum(LoggingLevelEnum);

function init() {
  if (settingSystemState.data === undefined) {
    return;
  }

  appMode.title = settingSystemState.data.app_mode;
  appMode.selectedValue = settingSystemState.data.app_mode;
  timezone.title = settingSystemState.data.app_timezone;
  timezone.selectedValue = settingSystemState.data.app_timezone;
  loggingLevel.title = settingSystemState.data.app_logging_level;
  loggingLevel.selectedValue = settingSystemState.data.app_logging_level;
}

init();

watch(
  () => JSON.stringify(settingSystemState.data),
  () => {
    init();
  },
);

watch(
  () => appMode.selectedValue,
  () => {
    if (settingSystemState.data === undefined || appMode.selectedValue === undefined) {
      return;
    }
    settingSystemState.data.app_mode = appMode.selectedValue as AppModeEnum;
  },
);

watch(
  () => timezone.selectedValue,
  () => {
    if (settingSystemState.data === undefined || timezone.selectedValue === undefined) {
      return;
    }
    settingSystemState.data.app_timezone = timezone.selectedValue as string;
  },
);

watch(
  () => loggingLevel.selectedValue,
  () => {
    if (settingSystemState.data === undefined || loggingLevel.selectedValue === undefined) {
      return;
    }
    settingSystemState.data.app_logging_level = loggingLevel.selectedValue as LoggingLevelEnum;
  },
);

function save() {
  settingSystemState.save();
}
</script>

<template>
  <div class="views-setting-container" v-if="settingSystemState.data !== undefined">
    <div class="views-setting-section">
      <span class="views-setting-section-title">ZetsuBou app</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Mode:&emsp;</span>
          <select-dropdown
            class="mx-1 w-72"
            :options-width-class="'w-72'"
            :origin="Origin.BottomLeft"
            :state="appMode"
            :options="appModeOptions"
            :is-auto-complete="true"
            :mode="SelectDropdownMode.Button" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Timezone:&emsp;</span>
          <select-dropdown
            class="mx-1 w-72"
            :options-width-class="'w-72'"
            :origin="Origin.BottomLeft"
            :state="timezone"
            :options="timezoneOptions"
            :is-auto-complete="true"
            :mode="SelectDropdownMode.Input" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Logging level:&emsp;</span>
          <select-dropdown
            class="mx-1 w-72"
            :options-width-class="'w-72'"
            :origin="Origin.BottomLeft"
            :state="loggingLevel"
            :options="loggingLevelOptions"
            :is-auto-complete="true"
            :mode="SelectDropdownMode.Input" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Security expired (minutes):&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.app_security_expired" />
        </div>
      </div>
    </div>
    <div class="views-setting-section">
      <span class="views-setting-section-title">Database</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">URL:&emsp;</span>
          <input
            class="views-setting-cell w-144"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.database_url" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Port:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.database_port" />
        </div>
      </div>
    </div>
    <div class="views-setting-section">
      <span class="views-setting-section-title">Redis</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">URL:&emsp;</span>
          <input
            class="views-setting-cell w-144"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.redis_url" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Port:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.redis_port" />
        </div>
      </div>
    </div>
    <div class="views-setting-section">
      <span class="views-setting-section-title">Elasticsearch</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">URLs:&emsp;</span>
          <input
            class="views-setting-cell w-144"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.elastic_urls" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Gallery index:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.elastic_index_gallery" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Video index:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.elastic_index_video" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Tag index:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.elastic_index_tag" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Port:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.elasticsearch_port" />
        </div>
      </div>
    </div>
    <div class="views-setting-section">
      <span class="views-setting-section-title">S3 storage</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Endpoint URLs:&emsp;</span>
          <input
            class="views-setting-cell w-144"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.storage_s3_endpoint_url" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Port:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.storage_s3_port" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Console port:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.storage_s3_console_port" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Access key ID:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.storage_s3_aws_access_key_id" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Secret access_key:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="password"
            autocomplete="new-password"
            v-model="settingSystemState.data.storage_s3_aws_secret_access_key" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Volume:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.storage_s3_volume" />
        </div>
      </div>
    </div>
    <div class="views-setting-section">
      <span class="views-setting-section-title">Airflow</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Host:&emsp;</span>
          <input
            class="views-setting-cell w-144"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.airflow_host" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Port:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.airflow_web_server_port" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Username:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="text"
            autocomplete="new-password"
            v-model="settingSystemState.data.airflow_username" />
        </div>
        <div class="views-setting-row">
          <span class="views-setting-cell w-64">Password:&emsp;</span>
          <input
            class="views-setting-cell w-72"
            type="password"
            autocomplete="new-password"
            v-model="settingSystemState.data.airflow_password" />
        </div>
        <div class="views-setting-row">
          <ripple-button class="flex btn btn-primary ml-auto" @click="save">Save</ripple-button>
        </div>
      </div>
    </div>
  </div>
</template>
