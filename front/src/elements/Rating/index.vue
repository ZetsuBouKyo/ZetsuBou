<script>
import Token from "./Token.vue";

export default {
  components: { Token },
  props: {
    max: {
      type: Number,
      default: 5,
    },
    filled: {
      type: Number,
      default: 0,
    },
  },
  setup(props) {
    return { ...props };
  },
};
</script>

<template>
  <span class="flex items-center">
    <token :isFilled="true" v-for="i in filled" :key="i"></token>
    <token v-for="i in max - filled" :key="i" />
  </span>
</template>
