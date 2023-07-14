<script setup lang="ts">
import { ButtonColorEnum } from "@/elements/Button/button.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";

export interface CrudTableButtonRow {
  id?: number;
  [key: string]: any;
}

export interface OnClick {
  (row: CrudTableButtonRow): void;
}

interface Props {
  text: string;
  row: CrudTableButtonRow;
  color: ButtonColorEnum;
  onClick: OnClick;
}
const props = withDefaults(defineProps<Props>(), {
  text: undefined,
  row: undefined,
  color: ButtonColorEnum.Primary,
  onClick: undefined,
});

const onClick = props.onClick;

function click(row: CrudTableButtonRow) {
  if (row !== undefined) {
    const data = JSON.parse(JSON.stringify(row));
    onClick(data);
  }
}
</script>

<template>
  <ripple-button class="mr-2 btn-icon cursor-pointer" :class="color" @click="click(row)">
    <div class="ml-2"><slot name="icon"></slot></div>
    <span class="ml-2 mr-4">{{ text }}</span>
  </ripple-button>
</template>
