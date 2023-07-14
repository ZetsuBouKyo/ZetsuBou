<script setup lang="ts">
import { onBeforeMount } from "vue";

import TopNav from "@/components/TopNav/index.vue";
import Message from "./Message.vue";

import { settingState } from "@/state/Setting/front";
import { userState } from "@/state/user";

onBeforeMount(() => {
  userState.init();
  settingState.init();
});
</script>

<template>
  <top-nav class="z-50" />
  <router-view class="text-gray-300" />
  <message />
</template>
