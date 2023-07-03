<template>
  <div class="w-10">
    <dropdown :select-class="''" :is-expand="false" :options-width-class="'w-72'">
      <template v-slot:select>
        <ripple-button class="focus:outline-none h-full rounded">
          <icon-mdi-bell-outline
            class="text-white mx-2 my-auto cursor-pointer hover:opacity-50"
            style="font-size: 1.4rem" />
        </ripple-button>
      </template>
      <template v-slot:options>
        <div class="flex flex-col divide-y divide-gray-500">
          <div class="flex flex-row p-4 text-sm">
            <span class="flex text-white font-bold my-auto">Notifications</span>
            <ripple-button class="flex ml-auto text-gray-300 rounded p-2 hover:opacity-50" @click="clearHistory">
              Clear
            </ripple-button>
          </div>
          <div class="flex flex-col max-h-72 overflow-y-scroll scrollbar-gray-900-2" v-if="state.clear > 0">
            <router-link
              class="flex flex-col bg-gray-900 pt-2 hover:opacity-50"
              :class="!msg.link ? 'cursor-default' : 'cursor-pointer'"
              v-for="(msg, i) in messageState.getHistory()"
              :to="msg.link !== undefined ? msg.link : ''"
              :key="msg.id + i">
              <span class="text-sm px-4 py-2">{{ msg.detail }}</span>
              <div class="flex ml-auto text-gray-300 text-xs px-4 py-2">Last updated: {{ msg.lastUpdated }}</div>
            </router-link>
          </div>
          <div class="flex flex-col" v-else>
            <span class="px-4 py-4 text-gray-500">Empty</span>
          </div>
        </div>
      </template>
    </dropdown>
  </div>
</template>

<script lang="ts">
import { reactive, watch } from "vue";

import Dropdown from "@/elements/Dropdown/Dropdown.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";

import { messageState } from "@/state/message";

export default {
  components: { Dropdown, RippleButton },
  setup() {
    const state = reactive({
      clear: messageState.getHistory().length,
    });

    watch(
      () => JSON.stringify(messageState.history),
      () => {
        state.clear = messageState.getHistory().length;
      },
    );

    function clearHistory() {
      messageState.clearHistory();
      state.clear = messageState.getHistory().length;
    }

    return { state, messageState, clearHistory };
  },
};
</script>
