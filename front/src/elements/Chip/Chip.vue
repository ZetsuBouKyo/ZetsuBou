<script setup lang="ts">
interface OnDelete {
  (title: string | number, value?: string | number | any, key?: number): void;
}

interface Props {
  title: string | number;
  value: string | number;
  index: number;
  onDelete: OnDelete;
}
const props = withDefaults(defineProps<Props>(), {
  title: undefined,
  value: undefined,
  index: undefined,
  onDelete: undefined,
});

function remove() {
  if (props.onDelete) {
    props.onDelete(props.title, props.value, props.index);
  }
}
</script>

<template>
  <span class="chip chip-dark">
    <button v-if="onDelete" class="mr-4 rounded-full focus:outline-none" @click="remove">✕</button>
    <span>{{ title }}</span>
  </span>
</template>
