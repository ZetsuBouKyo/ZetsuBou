<template>
  <div class="flex flex-row my-6">
    <span class="w-min my-1 3xl:py-2 py-1 text-gray-100">{{ fieldKey }}:&nbsp;&nbsp;</span>
    <div class="flex flex-wrap w-full text-gray-900">
      <ripple-anchor
        class="transition-colors duration-200 ease-in m-1 3xl:px-4 3xl:py-2 px-3 py-1 bg-gray-200 rounded-full max-w-full"
        :class="
          searchable ? 'cursor-pointer hover:bg-indigo-500 hover:text-gray-100 hover:border-white' : 'cursor-default'
        "
        v-for="(val, i) in fieldValues"
        :key="i"
        :href="searchable ? search(fieldKey, val) : undefined"
      >
        {{ val }}
      </ripple-anchor>
    </div>
  </div>
</template>

<script lang="ts">
import { PropType } from "vue";

import RippleAnchor from "@/elements/Anchor/RippleAnchor.vue";

export default {
  components: { RippleAnchor },
  props: {
    fieldKey: {
      type: Object as PropType<string>,
      required: true,
    },
    fieldValues: {
      type: Object as PropType<Array<string>>,
      required: true,
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
    function search(field: string, value: string) {
      return `${props.searchBaseUrl}?tag_field_1=${field}&tag_value_1=${value}`;
    }
    return { ...props, search };
  },
};
</script>
