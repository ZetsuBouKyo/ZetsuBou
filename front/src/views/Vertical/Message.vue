<template>
  <div class="fixed top-20 right-8 z-50">
    <div class="flex flex-col">
      <div class="w-64 p-4 my-1 animate-fade-in bg-black rounded-lg" v-for="(msg, i) in messageState.queue" :key="i">
        <span class="text-white">{{ msg.detail }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { messageState } from "@/state/message";

export default {
  setup() {
    return { messageState };
  },
};
</script>
