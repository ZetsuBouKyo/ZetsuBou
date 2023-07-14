<script setup lang="ts">
import { reactive } from "vue";

import RippleButton from "@/elements/Button/RippleButton.vue";

import { getToken } from "@/api/v1/token";

const state = reactive({
  email: undefined,
  password: undefined,
  expires: 30 as any,
  token: undefined,
});

function getNewToken() {
  const formData = new FormData();
  formData.append("username", state.email);
  formData.append("password", state.password);
  formData.append("expires", state.expires);

  getToken(formData).then((response) => {
    const data = response.data;
    if (data) {
      state.token = data.access_token;
    }
  });
}
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
        <div class="views-setting-row">
          <div class="views-setting-cell w-48" v-if="state.token">Token:</div>
          <span class="views-setting-cell w-96 break-all">{{ state.token }}</span>
        </div>
        <div class="views-setting-row">
          <ripple-button class="flex btn btn-primary ml-auto" @click="getNewToken">Get</ripple-button>
        </div>
      </div>
    </div>
  </div>
</template>
