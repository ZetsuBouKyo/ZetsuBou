<script setup lang="ts">
import CustomCircle from "./Circle.vue";
import Star from "./Star.vue";
interface Props {
  isFilled: boolean;
  shape: "STAR" | "CIRCLE";
}
const props = withDefaults(defineProps<Props>(), {
  isFilled: false,
  shape: "STAR",
});

let fill: string;
const shape = props.shape;
if (!props.isFilled) {
  fill = "none";
} else {
  fill = "currentColor";
}
</script>

<template>
  <svg
    :fill="fill"
    stroke="currentColor"
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="2"
    class="3xl:w-6 3xl:h-6 w-4 h-4 text-yellow-300"
    viewBox="0 0 24 24">
    <star v-if="shape === 'STAR'" />
    <custom-circle v-else-if="shape === 'CIRCLE'" />
  </svg>
</template>
