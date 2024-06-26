<script setup lang="ts">
import { PropType, reactive, watch } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownMode, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";
import { StepState } from "@/views/Vertical/Initialization/Step.interface";

import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import Step from "../Step.vue";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";

import { isEmail } from "@/utils/email";
import { getTimezoneOptions } from "@/utils/timezone";

const props = defineProps({
  step: {
    type: Object as PropType<StepState>,
    required: true,
  },
});

const step = props.step;

const state = reactive({ password: undefined, confirmedEmail: undefined, confirmedPassword: undefined });

const timezone = initSelectDropdownState() as SelectDropdownState;
const timezoneOptions = getTimezoneOptions();

watch(
  () => {
    return [
      step.setting.app_admin_name,
      step.setting.app_admin_email,
      step.setting.app_admin_password,
      state.password,
      timezone.selectedValue,
    ];
  },
  () => {
    if (step.setting.app_admin_email) {
      if (isEmail(step.setting.app_admin_email)) {
        state.confirmedEmail = true;
      } else {
        state.confirmedEmail = false;
        return;
      }
    } else {
      state.confirmedEmail = undefined;
      return;
    }
    if (step.setting.app_admin_password && state.password) {
      if (step.setting.app_admin_password === state.password) {
        state.confirmedPassword = true;
      } else {
        state.confirmedPassword = false;
        return;
      }
    } else {
      state.confirmedPassword = undefined;
      return;
    }
    if (step.setting.app_admin_name && timezone.selectedValue) {
      step.next = true;
    } else {
      step.next = false;
    }
  },
);
</script>

<template>
  <step :state="step">
    <template v-slot:body>
      <div class="views-setting-row-12">
        <span class="views-setting-cell w-48">Admin name:&emsp;</span>
        <input
          class="views-setting-cell w-72"
          type="text"
          autocomplete="new-password"
          v-model="step.setting.app_admin_name" />
      </div>
      <div class="views-setting-row-12">
        <span class="views-setting-cell w-48">Admin email:&emsp;</span>
        <input
          class="views-setting-cell w-72"
          type="text"
          autocomplete="new-password"
          v-model="step.setting.app_admin_email" />
        <span class="views-setting-cell text-blue-500" v-if="state.confirmedEmail === true">ok</span>
        <span class="views-setting-cell text-red-500" v-if="state.confirmedEmail === false">error</span>
      </div>
      <div class="views-setting-row-12">
        <span class="views-setting-cell w-48">Admin password:&emsp;</span>
        <input
          class="views-setting-cell w-72"
          type="password"
          autocomplete="new-password"
          v-model="step.setting.app_admin_password" />
      </div>
      <div class="views-setting-row-12">
        <span class="views-setting-cell w-48">Confirm password:&emsp;</span>
        <input class="views-setting-cell w-72" type="password" autocomplete="new-password" v-model="state.password" />
        <span class="views-setting-cell text-blue-500" v-if="state.confirmedPassword === true">ok</span>
        <span class="views-setting-cell text-red-500" v-if="state.confirmedPassword === false">error</span>
      </div>
      <div class="views-setting-row-12">
        <span class="views-setting-cell w-48">Timezone:&emsp;</span>
        <select-dropdown
          class="mx-1 w-72"
          :options-width-class="'w-72'"
          :origin="Origin.BottomLeft"
          :state="timezone"
          :options="timezoneOptions"
          :is-auto-complete="true"
          :mode="SelectDropdownMode.Input" />
      </div>
    </template>
  </step>
</template>
