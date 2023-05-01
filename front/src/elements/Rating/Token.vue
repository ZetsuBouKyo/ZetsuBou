<script>
import Star from "./Star.vue";
import CustomCircle from "./Circle.vue";

export default {
  components: { Star, CustomCircle },
  props: {
    isFilled: {
      type: Boolean,
      default: false,
    },
    shape: {
      type: "STAR" | "CIRCLE",
      default: "STAR",
    },
  },
  setup(props) {
    let fill;
    const shape = props.shape;
    if (!props.isFilled) {
      fill = "none";
    } else {
      fill = "currentColor";
    }
    return {
      fill,
      shape,
    };
  },
};
</script>

<template>
  <svg
    :fill="fill"
    stroke="currentColor"
    stroke-linecap="round"
    stroke-linejoin="round"
    stroke-width="2"
    class="3xl:w-6 3xl:h-6 w-4 h-4 text-yellow-300"
    viewBox="0 0 24 24"
  >
    <star v-if="shape === 'STAR'" />
    <custom-circle v-else-if="shape === 'CIRCLE'" />
  </svg>
</template>
