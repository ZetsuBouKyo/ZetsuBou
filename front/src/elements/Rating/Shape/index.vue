<script setup lang="ts">
import { RatingShapeEnum } from "../rating.interface";

import CustomCircle from "./Circle.vue";
import Star from "./Star.vue";
interface Props {
    isFilled: boolean;
    shape: RatingShapeEnum;
}
const props = withDefaults(defineProps<Props>(), {
    isFilled: false,
    shape: RatingShapeEnum.Star,
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
        viewBox="0 0 24 24"
    >
        <star v-if="shape === RatingShapeEnum.Star" />
        <custom-circle v-else-if="shape === RatingShapeEnum.Circle" />
    </svg>
</template>
