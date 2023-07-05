<template>
  <div class="flex flex-wrap text-gray-200 3xl:text-xl py-1">
    <ripple-anchor
      class="h-8 transition-colors duration-200 ease-in mx-2 my-1 3xl:px-4 3xl:py-2 px-3 py-1 rounded-full max-w-full truncate"
      :class="
        searchable
          ? 'cursor-pointer border border-gray-200 hover:border-indigo-500 hover:bg-indigo-500 hover:text-gray-100 '
          : 'cursor-default border border-gray-200'
      "
      v-for="(val, key) in labels"
      :key="key"
      :href="searchable ? search(val) : undefined">
      {{ val }}
    </ripple-anchor>
  </div>
</template>

<script lang="ts">
import RippleAnchor from "@/elements/Anchor/RippleAnchor.vue";

import { PropType } from "vue";

export default {
  components: { RippleAnchor },
  props: {
    labels: {
      type: Object as PropType<Array<string>>,
      default: [],
    },
    searchable: {
      type: Object as PropType<boolean>,
      default: true,
    },
    searchBaseUrl: {
      type: Object as PropType<string>,
      default: undefined,
    },
  },
  setup(props) {
    function search(label: string) {
      return `${props.searchBaseUrl}?label_1=${label}`;
    }
    return { ...props, search };
  },
};
</script>
