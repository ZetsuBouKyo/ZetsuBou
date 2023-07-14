<script setup lang="ts">
import Token from "./Token.vue";

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
    <token :isFilled="true" v-for="i in filled" :key="i"></token>
    <token v-for="i in max - filled" :key="i" />
  </span>
</template>
