<template>
  <span class="chip chip-dark">
    <button v-if="onDelete" class="mr-4 rounded-full focus:outline-none" @click="remove">✕</button>
    <span>{{ title }}</span>
  </span>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

export interface OnDelete {
  (title: string | number, value?: string | number, key?: number): void;
}

export default defineComponent({
  props: {
    title: {
      type: Object as PropType<string | number>,
      default: undefined,
    },
    value: {
      type: Object as PropType<string | number>,
      default: undefined,
    },
    index: {
      type: Object as PropType<number>,
      default: undefined,
    },
    onDelete: {
      type: Object as PropType<OnDelete>,
      default: undefined,
    },
  },
  setup(props) {
    function remove() {
      if (props.onDelete) {
        props.onDelete(props.title, props.value, props.index);
      }
    }
    return { ...props, remove };
  },
});
</script>
