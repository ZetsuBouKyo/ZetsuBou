<template>
  <ripple-button class="mr-2 btn-icon cursor-pointer" :class="color" @click="onClick(row)">
    <div class="ml-2"><slot name="icon"></slot></div>
    <span class="ml-2 mr-4">{{ text }}</span>
  </ripple-button>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

import { ButtonColorEnum } from "@/elements/Button/button.ts";

export interface CrudTableButtonRow {
  id?: number;
  [key: string]: any;
}

export interface OnClick {
  (row: CrudTableButtonRow): void;
}

export default defineComponent({
  props: {
    text: {
      type: Object as PropType<string>,
      default: undefined,
    },
    row: {
      type: Object as PropType<CrudTableButtonRow>,
      default: undefined,
    },
    color: { type: Object as PropType<ButtonColorEnum>, default: ButtonColorEnum.Primary },
    onClick: {
      type: Object as PropType<OnClick>,
      default: undefined,
    },
  },
  setup(props) {
    return { ...props };
  },
});
</script>
