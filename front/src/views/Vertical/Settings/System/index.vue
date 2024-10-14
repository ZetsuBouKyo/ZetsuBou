<script setup lang="ts">
import { ref, watch } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownOption } from "@/elements/Dropdown/SelectDropdown.interface";
import { AppModeEnum, LoggingLevelEnum } from "@/interface/setting";

import RippleButton from "@/elements/Button/RippleButton.vue";
import InputSelectDropdown from "@/elements/Dropdown/InputSelectDropdown.vue";
import RippleButtonSelectDropdown from "@/elements/Dropdown/RippleButtonSelectDropdown.vue";

import { getOptionsFromEnum } from "@/elements/Dropdown/SelectDropdown";
import { settingSystemState } from "@/state/Setting/system";

import { getTimezoneOptions } from "@/utils/timezone";

settingSystemState.init();

const appModeTitle = ref(settingSystemState?.data?.app_mode);
const appModeSelectedValue = ref(settingSystemState?.data?.app_mode);
const appModeOptions = ref(getOptionsFromEnum(AppModeEnum));
function selectAppMode(opt: SelectDropdownOption) {
    settingSystemState.data.app_mode = opt.value as AppModeEnum;
}

watch(
    () => {
        return JSON.stringify(settingSystemState.data);
    },
    () => {
        if (settingSystemState.data === undefined) {
            return;
        }
        appModeTitle.value = settingSystemState?.data?.app_mode;
        appModeSelectedValue.value = settingSystemState?.data?.app_mode;
    },
);

const timezoneTitle = ref("");
const timezoneSelectedValue = ref(undefined);
const timezoneDefaultOptions = ref(getTimezoneOptions());
const timezoneOptions = ref(getTimezoneOptions());
function selectTimezone(opt: SelectDropdownOption) {
    if (settingSystemState.data === undefined || opt.value === undefined) {
        return;
    }
    settingSystemState.data.app_timezone = opt.value as string;
}

const loggingLevelTitle = ref("");
const loggingLevelSelectedValue = ref(undefined);
const loggingLevelDefaultOptions = ref(getOptionsFromEnum(LoggingLevelEnum));
const loggingLevelOptions = ref(getOptionsFromEnum(LoggingLevelEnum));
function selectLoggingLevel(opt: SelectDropdownOption) {
    if (settingSystemState.data === undefined || loggingLevelSelectedValue.value === undefined) {
        return;
    }
    settingSystemState.data.app_logging_level = loggingLevelSelectedValue.value as LoggingLevelEnum;
}

function init() {
    if (settingSystemState.data === undefined) {
        return;
    }
    timezoneTitle.value = settingSystemState.data.app_timezone as string;
    timezoneSelectedValue.value = settingSystemState.data.app_timezone as string;
    loggingLevelTitle.value = settingSystemState.data.app_logging_level;
    loggingLevelSelectedValue.value = settingSystemState.data.app_logging_level;
}

init();

watch(
    () => JSON.stringify(settingSystemState.data),
    () => {
        init();
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
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Mode:&emsp;</span>
                    <ripple-button-select-dropdown
                        class="mx-1 w-72"
                        v-model:title="appModeTitle"
                        v-model:selected-value="appModeSelectedValue"
                        v-model:options="appModeOptions"
                        :options-width-class="'w-72'"
                        :origin="Origin.BottomLeft"
                        :on-select="selectAppMode"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Timezone:&emsp;</span>
                    <input-select-dropdown
                        class="mx-1 w-72"
                        v-model:title="timezoneTitle"
                        v-model:selected-value="timezoneSelectedValue"
                        v-model:default-options="timezoneDefaultOptions"
                        v-model:options="timezoneOptions"
                        :options-width-class="'w-72'"
                        :origin="Origin.BottomLeft"
                        :on-select="selectTimezone"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Logging level:&emsp;</span>
                    <input-select-dropdown
                        class="mx-1 w-72"
                        v-model:title="loggingLevelTitle"
                        v-model:selected-value="loggingLevelSelectedValue"
                        v-model:default-options="loggingLevelDefaultOptions"
                        v-model:options="loggingLevelOptions"
                        :options-width-class="'w-72'"
                        :origin="Origin.BottomLeft"
                        :on-select="selectLoggingLevel"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Security expired (minutes):&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.app_security_expired"
                    />
                </div>
            </div>
        </div>
        <div class="views-setting-section">
            <span class="views-setting-section-title">Database</span>
            <div class="views-setting-rows">
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">URL:&emsp;</span>
                    <input
                        class="views-setting-cell w-144"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.database_url"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Port:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.database_port"
                    />
                </div>
            </div>
        </div>
        <div class="views-setting-section">
            <span class="views-setting-section-title">Redis</span>
            <div class="views-setting-rows">
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">URL:&emsp;</span>
                    <input
                        class="views-setting-cell w-144"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.redis_url"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Port:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.redis_port"
                    />
                </div>
            </div>
        </div>
        <div class="views-setting-section">
            <span class="views-setting-section-title">Elasticsearch</span>
            <div class="views-setting-rows">
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">URLs:&emsp;</span>
                    <input
                        class="views-setting-cell w-144"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.elastic_urls"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Gallery index:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.elastic_index_gallery"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Video index:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.elastic_index_video"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Tag index:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.elastic_index_tag"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Port:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.elasticsearch_port"
                    />
                </div>
            </div>
        </div>
        <div class="views-setting-section">
            <span class="views-setting-section-title">S3 storage</span>
            <div class="views-setting-rows">
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Endpoint URLs:&emsp;</span>
                    <input
                        class="views-setting-cell w-144"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.storage_s3_endpoint_url"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Port:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.storage_s3_port"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Console port:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.storage_s3_console_port"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Access key ID:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.storage_s3_aws_access_key_id"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Secret access_key:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="password"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.storage_s3_aws_secret_access_key"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Volume:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.storage_s3_volume"
                    />
                </div>
            </div>
        </div>
        <div class="views-setting-section">
            <span class="views-setting-section-title">Airflow</span>
            <div class="views-setting-rows">
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Host:&emsp;</span>
                    <input
                        class="views-setting-cell w-144"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.airflow_host"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Port:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.airflow_web_server_port"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Username:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="text"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.airflow_username"
                    />
                </div>
                <div class="views-setting-row-12">
                    <span class="views-setting-cell w-64">Password:&emsp;</span>
                    <input
                        class="views-setting-cell w-72"
                        type="password"
                        autocomplete="new-password"
                        v-model="settingSystemState.data.airflow_password"
                    />
                </div>
                <div class="views-setting-row-12">
                    <ripple-button class="flex btn btn-primary ml-auto" @click="save">Save</ripple-button>
                </div>
            </div>
        </div>
    </div>
</template>
