<script lang="ts">
import { PropType, reactive } from "vue";

import Modal from "./Modal.vue";

export interface ConfirmModalState {
  popout: boolean;
}

export interface OnOpen {
  (): void;
}

export interface OnClose {
  (): void;
}

export interface OnConfirm {
  (): void;
}

export default {
  components: { Modal },
  props: {
    state: {
      type: Object as PropType<ConfirmModalState>,
      default: () => {
        return reactive<ConfirmModalState>({
          popout: false,
        });
      },
    },
    title: {
      type: Object as PropType<string>,
      default: "Confirm",
    },
    message: {
      type: Object as PropType<string>,
      default: "Are you sure?",
    },
    onOpen: {
      type: Object as PropType<OnOpen>,
      default: undefined,
    },
    onClose: {
      type: Object as PropType<OnClose>,
      default: undefined,
    },
    onConfirm: {
      type: Object as PropType<OnConfirm>,
      default: undefined,
    },
  },
  setup(props) {
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

    function confirm() {
      state.popout = false;
      if (props.onConfirm !== undefined) {
        props.onConfirm();
      }
    }

    return { ...props, open, close, confirm };
  },
};
</script>

<template>
  <modal :state="state" :title="title" :on-close="onClose" class="w-1/2 lg:w-1/3 top-32 left-1/4 lg:left-1/3">
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
