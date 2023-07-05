<template>
  <div class="fixed top-20 right-8 z-50">
    <div class="flex flex-col">
      <div class="w-64 p-4 my-1 animate-fade-in bg-black rounded-lg" v-for="(msg, i) in messageState.queue" :key="i">
        <div class="flex flex-col" @mouseenter="lock(msg)" @mouseleave="unlock(msg)">
          <span class="flex text-white">{{ msg.detail }}</span>
          <span class="flex pt-2 text-gray-300 text-xs ml-auto">last updated: {{ msg.lastUpdated }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Message, messageState } from "@/state/message";

export default {
  setup() {
    function lock(message: Message) {
      message.lock = true;
    }

    function unlock(message: Message) {
      message.lock = false;
      if (message.timeout === undefined) {
        messageState.shiftQueue(message.id);
      }
    }

    return { messageState, lock, unlock };
  },
};
</script>
