<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRoute } from "vue-router";

import { SourceState } from "@/interface/source";
import { OnOverwrite } from "./interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Modal from "@/elements/Modal/Modal.vue";

import { initRippleButtonState } from "@/elements/Button/RippleButton";
import { messageState } from "@/state/message";

interface Props {
  title?: string;
  state?: SourceState<any>;
  onOverwrite?: OnOverwrite;
  saveMessage?: string;
  resetMessage?: string;
}
const props = withDefaults(defineProps<Props>(), {
  title: "Text Editor",
  state: undefined,
  onOverwrite: undefined,
  saveMessage: "Saved",
  resetMessage: "Reset",
});

const route = useRoute();

const editor = ref();
const state = props.state;
const onOverwrite = props.onOverwrite;

const privateState = reactive<{ json: string }>({
  json: undefined,
});

const saveState = initRippleButtonState();
function saved() {
  editor.value.close();
  messageState.pushWithLink(props.saveMessage, route.path);
}
function save() {
  saveState.lock();
  overwrite().then((status) => {
    if (!status) {
      return;
    }
    state.save(saved).finally(() => {
      saveState.unlock();
    });
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
  window.scrollTo(0, 0);
  editor.value.open();
  if (!privateState.json) {
    privateState.json = JSON.stringify(state.data, null, 4);
  }
}

defineExpose({ open });
</script>

<template>
  <modal ref="editor" :title="title" class="w-1/2 h-3/4 top-12 left-1/4">
    <div class="modal-row-h-full">
      <textarea v-model="privateState.json" class="modal-textarea h-full" />
    </div>
    <div class="modal-row">
      <div class="flex ml-auto">
        <ripple-button class="flex mr-2 btn btn-primary" @click="reset"> Reset </ripple-button>
        <ripple-button class="flex mr-2 btn btn-primary" @click="overwrite"> Overwrite </ripple-button>
        <ripple-button class="flex btn btn-primary" :state="saveState" @click="save"> Save </ripple-button>
      </div>
    </div>
  </modal>
</template>
