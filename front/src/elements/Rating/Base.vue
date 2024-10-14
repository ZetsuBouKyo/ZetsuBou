<script setup lang="ts">
import Shape from "./Shape/index.vue";

interface Props {
    max: number;
    filled: number;
}
withDefaults(defineProps<Props>(), {
    max: 5,
    filled: 0,
});
</script>

<template>
    <span class="flex items-center">
        <shape :isFilled="true" v-for="i in filled" :key="i" />
        <shape v-for="i in max - filled" :key="i" />
    </span>
</template>
