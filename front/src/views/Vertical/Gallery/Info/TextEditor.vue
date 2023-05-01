<template>
  <modal ref="editor" :title="'Gallery JSON Editor'" class="w-1/2 h-1/2 top-1/4 left-1/4">
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
import { reactive, ref } from "vue";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Modal from "@/elements/Modal/Modal.vue";

import { galleryState } from "@/state/gallery";
import { messageState } from "@/state/message";

export default {
  components: { Modal, RippleButton },
  setup() {
    const editor = ref();

    const privateState = reactive<{ json: string }>({
      json: undefined,
    });

    function save() {
      overwrite().then((status) => {
        if (!status) {
          return;
        }
        galleryState.save().then(() => {
          editor.value.close();
          messageState.push("Saved");
        });
      });
    }

    async function overwrite() {
      return galleryState.reset().then(() => {
        try {
          if (privateState.json === undefined || privateState.json.trim() === "") {
            privateState.json = JSON.stringify(galleryState.data, null, 4);
            return true;
          }
          let data = JSON.parse(privateState.json);
          if (data.attributes !== undefined) {
            galleryState.data.attributes = data.attributes;
          }
          if (data.tags !== undefined) {
            galleryState.data.tags = data.tags;
          }
          if (data.labels !== undefined) {
            galleryState.data.labels = data.labels;
          }
          privateState.json = JSON.stringify(galleryState.data, null, 4);
          return true;
        } catch (error) {
          messageState.push(error.message);
          return false;
        }
      });
    }

    function reset() {
      galleryState.reset().then(() => {
        privateState.json = JSON.stringify(galleryState.data, null, 4);
        messageState.push("Reset");
      });
    }

    function open() {
      editor.value.open();
    }

    return { editor, privateState, save, overwrite, reset, open };
  },
};
</script>
