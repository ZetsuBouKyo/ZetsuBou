<template>
  <ripple-button
    class="views-setting-action-ripple-button"
    :class="
      route.path === path ? 'views-setting-action-ripple-button-active' : 'views-setting-action-ripple-button-inactive'
    "
  >
    <a class="views-setting-action" :href="path">
      <slot></slot>
      <span class="views-setting-sub-action">&emsp;&emsp;&emsp;{{ title }}</span>
    </a>
  </ripple-button>
</template>

<script lang="ts">
import { PropType } from "vue";
import { useRoute } from "vue-router";

export default {
  props: {
    path: {
      type: Object as PropType<string>,
      default: undefined,
    },
    title: {
      type: Object as PropType<string>,
      default: undefined,
    },
  },
  setup(props) {
    const route = useRoute();
    return { ...props, route };
  },
};
</script>
