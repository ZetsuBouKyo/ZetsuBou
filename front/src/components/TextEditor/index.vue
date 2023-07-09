<template>
  <modal ref="editor" :title="title" class="w-1/2 h-3/4 top-12 left-1/4">
    <div class="modal-row-h-full">
      <textarea v-model="privateState.json" class="modal-textarea h-full" />
    </div>
    <div class="modal-row">
      <div class="flex ml-auto">
        <ripple-button class="flex mr-2 btn btn-primary" @click="reset"> Reset </ripple-button>
        <ripple-button class="flex mr-2 btn btn-primary" @click="overwrite"> Overwrite </ripple-button>
        <ripple-button class="flex btn btn-primary" @click="save"> Save </ripple-button>
      </div>
    </div>
  </modal>
</template>

<script lang="ts">
import { PropType, reactive, ref } from "vue";
import { useRoute } from "vue-router";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Modal from "@/elements/Modal/Modal.vue";

import { SourceState } from "@/interface/source";

import { messageState } from "@/state/message";

export interface OnOverwrite {
  (state: SourceState<any>, data: any): void;
}

export default {
  components: { Modal, RippleButton },
  props: {
    title: {
      type: Object as PropType<string>,
      default: "Text Editor",
    },
    state: {
      type: Object as PropType<SourceState<any>>,
      default: undefined,
    },
    onOverwrite: {
      type: Object as PropType<OnOverwrite>,
      default: undefined,
    },
    saveMessage: {
      type: Object as PropType<string>,
      default: "Saved",
    },
    resetMessage: {
      type: Object as PropType<string>,
      default: "Reset",
    },
  },
  setup(props) {
    const route = useRoute();

    const editor = ref();
    const state = props.state;
    const onOverwrite = props.onOverwrite;

    const privateState = reactive<{ json: string }>({
      json: undefined,
    });

    function saved() {
      editor.value.close();
      messageState.pushWithLink(props.saveMessage, route.path);
    }

    function save() {
      overwrite().then((status) => {
        if (!status) {
          return;
        }
        state.save(saved).then(() => {});
      });
    }

    async function overwrite() {
      return state.reset().then(() => {
        try {
          if (privateState.json === undefined || privateState.json.trim() === "") {
            privateState.json = JSON.stringify(state.data, null, 4);
            return true;
          }
          let data = JSON.parse(privateState.json);
          onOverwrite(state, data);
          privateState.json = JSON.stringify(state.data, null, 4);
          return true;
        } catch (error) {
          messageState.pushWithLink(error.message, route.path);
          return false;
        }
      });
    }

    function reset() {
      state.reset().then(() => {
        privateState.json = JSON.stringify(state.data, null, 4);
        messageState.pushWithLink(props.resetMessage, route.path);
      });
    }

    function open() {
      editor.value.open();
      if (!privateState.json) {
        privateState.json = JSON.stringify(state.data, null, 4);
      }
    }

    return { ...props, editor, privateState, save, overwrite, reset, open };
  },
};
</script>
