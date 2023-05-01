<template>
  <svg-editor :tagger="state" />
  <play-panel :tagger="state" />
</template>

<script>
import { reactive } from "vue";

import PlayPanel from "./PlayPanel.vue";
import SvgEditor from "./SvgEditor/index.vue";

export default {
  components: { PlayPanel, SvgEditor },
  setup() {
    const state = reactive({
      isTagger: false,
      activateTagger: () => {
        state.isTagger = true;
      },
      closeTagger: () => {
        state.isTagger = false;
      },
      toggleTagger: () => {
        state.isTagger = !state.isTagger;
      },
    });
    return { state };
  },
};
</script>
