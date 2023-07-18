<script setup lang="ts">
import { ref } from "vue";

import Modal from "./Modal.vue";

interface Props {
  title: string;
  message: string;
  onOpen: () => void;
  onClose: () => void;
  onConfirm: () => void;
}

const props = withDefaults(defineProps<Props>(), {
  title: "Confirm",
  message: "Are you sure?",
  onOpen: undefined,
  onClose: undefined,
  onConfirm: undefined,
});

const modalComponent = ref();

function open() {
  if (props.onOpen !== undefined) {
    props.onOpen();
  }
  modalComponent.value.open();
}

function close() {
  if (props.onClose !== undefined) {
    props.onClose();
  }
  modalComponent.value.close();
}

function confirm() {
  if (props.onConfirm !== undefined) {
    props.onConfirm();
  }
  modalComponent.value.close();
}

defineExpose({ open, close });
</script>

<template>
  <modal ref="modalComponent" :title="title" :on-close="onClose" class="w-1/2 lg:w-1/3 top-32 left-1/4 lg:left-1/3">
    <div class="flex h-full 3xl:px-6 px-3 py-2 text-gray-100">
      <span>{{ message }}</span>
    </div>
    <div class="flex flex-col p-2 items-center">
      <div class="flex ml-auto">
        <button class="flex my-2 mr-2 btn btn-primary" @click="close">Cancel</button>
        <button class="flex my-2 mr-2 btn btn-primary" @click="confirm">Ok</button>
      </div>
    </div>
  </modal>
</template>
