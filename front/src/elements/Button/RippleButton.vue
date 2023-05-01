<template>
  <button ref="bt" class="relative overflow-hidden" type="button" @click="rippleEffect">
    <slot></slot>
    <span ref="ripple" :class="state.isRipple ? 'zetsubou-ripple' : 'hidden'"></span>
  </button>
</template>

<script>
import { ref, reactive } from "vue";
export default {
  setup() {
    const bt = ref(null);
    const ripple = ref(null);
    const state = reactive({
      isRipple: false,
    });
    function rippleEffect(event) {
      state.isRipple = true;
      const btn = bt.value;
      const circle = ripple.value;
      const diameter = Math.max(btn.clientWidth, btn.clientHeight);
      const radius = diameter / 2;

      const bounds = btn.getBoundingClientRect();
      const x = event.clientX - bounds.left;
      const y = event.clientY - bounds.top;

      circle.style.width = circle.style.height = `${diameter}px`;
      circle.style.left = `${x - radius}px`;
      circle.style.top = `${y - radius}px`;

      setTimeout(() => {
        state.isRipple = false;
      }, 600);
    }
    return { state, bt, ripple, rippleEffect };
  },
};
</script>
