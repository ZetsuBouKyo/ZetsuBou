<template>
  <top-nav class="z-50" />
  <router-view class="text-gray-300" />
  <message />
</template>

<script>
import { onBeforeMount } from "vue";

import { settingState } from "@/state/setting";
import { userState } from "@/state/user";

import TopNav from "@/components/TopNav/index.vue";
import Message from "./Message.vue";

export default {
  components: { TopNav, Message },
  setup() {
    onBeforeMount(() => {
      userState.init();
      settingState.init();
    });
  },
};
</script>
