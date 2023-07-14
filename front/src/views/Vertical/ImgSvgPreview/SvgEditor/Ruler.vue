<template></template>

<script setup lang="ts">
import { PropType } from "vue";

import { SVG } from "./svg.interface";

const props = defineProps({
  svg: {
    type: Object as PropType<SVG>,
    required: true,
  },
});
</script>
