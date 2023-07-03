<template>
  <div class="lg:flex hidden flex-row-reverse">
    <ripple-button class="flex mt-4 ml-4 btn btn-primary" @click="state.openGallery"> Open </ripple-button>
    <ripple-button class="flex mt-4 ml-4 btn btn-primary" @click="state.openTextEditor"> JSON </ripple-button>
    <ripple-button class="flex mt-4 ml-4 btn btn-primary" @click="state.openEditor"> Edit </ripple-button>
    <ripple-button class="flex mt-4 ml-4 btn btn-danger" @click="state.openConfirmDeleteMessage">
      Delete
    </ripple-button>
  </div>
</template>

<script lang="ts">
import { PropType } from "vue";

import RippleButton from "@/elements/Button/RippleButton.vue";

import { ControlPanelState } from "./ControlPanel.d";

export default {
  components: { RippleButton },
  props: {
    state: {
      type: Object as PropType<ControlPanelState>,
      default: undefined,
    },
  },
  setup(props) {
    return { ...props };
  },
};
</script>
