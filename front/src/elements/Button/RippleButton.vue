<script setup lang="ts">
import { reactive, ref } from "vue";

import { RippleButtonState } from "./RippleButton.interface";

interface Props {
    state?: RippleButtonState;
    disabled: boolean;
}
const props = withDefaults(defineProps<Props>(), { state: undefined, disabled: false });

const bt = ref(null);
const ripple = ref(null);
const privateState = reactive({
    isRipple: false,
});
function rippleEffect(event: any) {
    privateState.isRipple = true;
    const btn = bt.value;
    if (btn === undefined || btn === null) {
        return;
    }
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
        privateState.isRipple = false;
    }, 600);
}

function isDisabled() {
    if (props.state && props.state.data !== undefined && props.state.data.lock) {
        return true;
    }

    return props.disabled;
}
</script>

<template>
    <button
        ref="bt"
        class="relative overflow-hidden focus:outline-none"
        type="button"
        @click="rippleEffect"
        :disabled="isDisabled()"
    >
        <slot></slot>
        <span ref="ripple" :class="privateState.isRipple ? 'zetsubou-ripple' : 'hidden'"></span>
    </button>
</template>
