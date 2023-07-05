<template></template>

<script lang="ts">
import { PropType } from "vue";

import { SVG } from "./svg.d";

export default {
  props: {
    svg: {
      type: Object as PropType<SVG>,
      default: undefined,
    },
  },
  setup(props) {
    return { ...props };
  },
};
</script>
