<template>
  <div class="flex flex-col">
    <ripple-button
      class="views-setting-action-ripple-button views-setting-action-ripple-button-inactive"
      @click="toggle">
      <div class="views-setting-action">
        <slot name="icon"></slot>
        <span class="views-setting-action-title">{{ title }}</span>
        <icon-ic-round-expand-more class="ml-auto self-center" v-if="!state.toggle" />
        <icon-ic-round-expand-less class="ml-auto self-center" v-else />
      </div>
    </ripple-button>
    <div class="flex flex-col" v-if="state.toggle">
      <setting-sub-action :title="option.title" :path="option.path" v-for="(option, key) in options" :key="key" />
    </div>
  </div>
</template>

<script lang="ts">
import { PropType, reactive, watch } from "vue";
import { useRoute } from "vue-router";

import RippleButton from "@/elements/Button/RippleButton.vue";

import SettingSubAction from "./SettingSubAction.vue";

interface Option {
  title: string;
  path: string;
}

export default {
  components: { RippleButton, SettingSubAction },
  props: {
    title: {
      type: Object as PropType<string>,
      default: undefined,
    },
    options: {
      type: Object as PropType<Array<Option>>,
      default: [],
    },
  },
  setup(props) {
    const route = useRoute();
    const state = reactive({ toggle: false });

    function checkPath() {
      for (let option of props.options) {
        if (option.path === route.path) {
          state.toggle = true;
          return;
        }
      }
      state.toggle = false;
    }
    checkPath();
    watch(
      () => JSON.stringify(route.path),
      () => {
        checkPath();
      },
    );

    function toggle() {
      state.toggle = !state.toggle;
    }

    return { ...props, state, toggle };
  },
};
</script>
