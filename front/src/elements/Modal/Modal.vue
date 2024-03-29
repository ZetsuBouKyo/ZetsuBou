<script setup lang="ts">
import { reactive } from "vue";

import { ModalPosition } from "./Modal.interface";

interface ModalState {
  popout: boolean;
  [key: string]: any;
}

interface OnOpen {
  (): void;
}

interface OnClose {
  (): void;
}

interface Props {
  state: ModalState;
  title: string;
  isScrollable: boolean;
  position: ModalPosition;
  onOpen: OnOpen;
  onClose: OnClose;
}
const props = withDefaults(defineProps<Props>(), {
  state: () =>
    reactive<ModalState>({
      popout: false,
    }),
  title: "Message",
  isScrollable: false,
  position: ModalPosition.absolute,
  onOpen: undefined,
  onClose: undefined,
});

const state = props.state;

function open() {
  state.popout = true;
  if (props.onOpen !== undefined) {
    props.onOpen();
  }
}

function close() {
  state.popout = false;
  if (props.onClose !== undefined) {
    props.onClose();
  }
}

defineExpose({ open, close });
</script>

<template>
  <div class="flex flex-col bg-opacity-0 z-50" :class="position" v-if="state.popout">
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
    <div class="z-50 flex flex-col w-full h-full bg-gray-800 rounded-lg shadow-black animate-scale-in-center mb-8">
      <div class="flex flex-row w-full mx-auto items-center p-2 text-white bg-gray-900 rounded-t-lg 3xl:text-2xl">
        <span class="flex ml-2">{{ title }}</span>
        <span class="flex ml-auto mx-2 px-2 hover:bg-gray-100 hover:text-gray-900 rounded cursor-pointer" @click="close"
          >✕</span
        >
      </div>
      <div
        class="flex flex-col w-full py-1"
        :class="isScrollable ? 'overflow-y-scroll scrollbar-gray-100-2 max-h-80v' : 'h-full'">
        <slot></slot>
      </div>
    </div>
  </div>
</template>
