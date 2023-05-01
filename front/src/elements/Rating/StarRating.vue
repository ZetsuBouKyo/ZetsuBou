<template>
  <div v-if="filled !== null && filled !== undefined">
    <rating :filled="filled" />
  </div>
  <div v-else>
    <rating :filled="0" />
  </div>
</template>

<script lang="ts">
import Rating from "./index.vue";

export default {
  components: { Rating },
  props: {
    filled: {
      type: Number,
      default: undefined,
    },
  },
  setup(props) {
    return { ...props };
  },
};
</script>
