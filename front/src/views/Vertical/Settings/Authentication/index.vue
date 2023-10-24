<script setup lang="ts">
import { reactive, watch } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownMode, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";

import { getScopesStartsWith } from "@/api/v1/scope";
import { getToken } from "@/api/v1/token";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";

import { JWTParser } from "@/utils/jwt";

const state = reactive({
  email: undefined,
  password: undefined,
  expires: 30 as any,
  token: undefined,
  scopes: [],
  header: undefined,
  payload: undefined,
});

function getNewToken() {
  const scope = state.scopes.join(" ");

  const formData = new FormData();
  formData.append("username", state.email);
  formData.append("password", state.password);
  formData.append("expires", state.expires);
  formData.append("scope", scope);

  getToken(formData).then((response) => {
    const data = response.data;
    if (data) {
      state.token = data.access_token;
      const parser = new JWTParser(state.token);
      state.header = parser.headerString;
      state.payload = parser.payloadString;
    }
  });
}

const scopes = initSelectDropdownState() as SelectDropdownState;
const onGetScopes = (param: any) => {
  param.name = "";
  return getScopesStartsWith(param);
};
function onGetScopesToOptions(data: { id: number; name: string }) {
  return { title: data.name, value: data.id };
}
watch(
  () => scopes.chips.length,
  () => {
    state.scopes = [];
    for (const chip of scopes.chips) {
      state.scopes.push(chip.title as string);
    }
  },
);
</script>

<template>
  <div class="views-setting-container">
    <div class="views-setting-section">
      <span class="views-setting-section-title">Token</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <div class="views-setting-cell w-48">Email address:</div>
          <input class="views-setting-cell w-72" type="text" v-model="state.email" />
        </div>
        <div class="views-setting-row">
          <div class="views-setting-cell w-48">Password:</div>
          <input class="views-setting-cell w-72" type="password" autocomplete="new-password" v-model="state.password" />
        </div>
        <div class="views-setting-row">
          <div class="views-setting-cell w-48">Expires in minutes:</div>
          <input class="views-setting-cell w-72" :placeholder="state.expires" type="text" v-model="state.expires" />
        </div>
        <div class="views-setting-row-base items-start">
          <div class="views-setting-cell w-48 my-4">Scopes:</div>
          <select-dropdown
            class="flex-1 ml-1"
            :options-width-class="'w-64'"
            :origin="Origin.BottomLeft"
            :state="scopes"
            :enable-input-chips-enter-event="false"
            :on-get="onGetScopes"
            :on-get-to-options="onGetScopesToOptions"
            :mode="SelectDropdownMode.InputChips" />
        </div>
        <div class="views-setting-row">
          <ripple-button class="flex btn btn-primary ml-auto" @click="getNewToken">Get</ripple-button>
        </div>
        <div class="views-setting-row-base items-start" v-if="state.token">
          <div class="views-setting-cell w-48">Token:</div>
          <div class="flex w-96 2xl:w-200 break-all">{{ state.token }}</div>
        </div>
        <div class="views-setting-row-base items-start" v-if="state.header">
          <div class="views-setting-cell w-48">Token Header:</div>
          <pre>{{ state.header }}</pre>
        </div>
        <div class="views-setting-row-base items-start" v-if="state.payload">
          <div class="views-setting-cell w-48">Token Payload:</div>
          <pre>{{ state.payload }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>
