<template>
  <ripple-button class="mr-2 btn-icon cursor-pointer" :class="color" @click="click(row)">
    <div class="ml-2"><slot name="icon"></slot></div>
    <span class="ml-2 mr-4">{{ text }}</span>
  </ripple-button>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

import { ButtonColorEnum } from "@/elements/Button/button";

import RippleButton from "@/elements/Button/RippleButton.vue";

export interface CrudTableButtonRow {
  id?: number;
  [key: string]: any;
}

export interface OnClick {
  (row: CrudTableButtonRow): void;
}

export default defineComponent({
  components: { RippleButton },
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
    const onClick = props.onClick;

    function click(row: CrudTableButtonRow) {
      if (row !== undefined) {
        const data = JSON.parse(JSON.stringify(row));
        onClick(data);
      }
    }
    return { ...props, click };
  },
});
</script>
