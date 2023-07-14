<script setup lang="ts">
import { PropType } from "vue";

import { AppModeEnum } from "@/interface/setting";
import { ControlPanelState } from "./ControlPanel.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";

import { settingState } from "@/state/Setting/front";

defineProps({
  state: {
    type: Object as PropType<ControlPanelState>,
    required: true,
  },
});
</script>

<template>
  <div class="lg:flex hidden flex-row-reverse">
    <ripple-button
      class="flex mt-4 ml-4 btn btn-primary"
      @click="state.openGallery"
      v-if="settingState.data && settingState.data.app_mode === AppModeEnum.Standalone">
      Open
    </ripple-button>
    <ripple-button class="flex mt-4 ml-4 btn btn-primary" @click="state.openTextEditor"> JSON </ripple-button>
    <ripple-button class="flex mt-4 ml-4 btn btn-primary" @click="state.openEditor"> Edit </ripple-button>
    <ripple-button class="flex mt-4 ml-4 btn btn-danger" @click="state.openConfirmDeleteMessage">
      Delete
    </ripple-button>
  </div>
</template>
