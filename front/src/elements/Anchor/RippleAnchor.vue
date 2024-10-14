<script setup lang="ts">
import { reactive, ref } from "vue";

const ripple = ref(null);
const state = reactive({
    isRipple: false,
});
function rippleEffect(event: any) {
    state.isRipple = true;
    const btn = event.target;
    const circle = ripple.value;
    const diameter = Math.max(btn.clientWidth, btn.clientHeight);
    const radius = diameter / 2;

    const bounds = event.target.getBoundingClientRect();
    const x = event.clientX - bounds.left;
    const y = event.clientY - bounds.top;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${x - radius}px`;
    circle.style.top = `${y - radius}px`;

    setTimeout(() => {
        state.isRipple = false;
    }, 600);
}
</script>

<template>
    <a class="relative overflow-hidden" type="button" @click="rippleEffect">
        <slot><a></a></slot>
        <span ref="ripple" class="z-50" :class="state.isRipple ? 'zetsubou-ripple' : 'hidden'"></span>
    </a>
</template>
