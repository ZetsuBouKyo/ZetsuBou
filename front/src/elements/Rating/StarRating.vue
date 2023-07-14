<script setup lang="ts">
import Rating from "./index.vue";

interface Props {
  filled: number;
}
withDefaults(defineProps<Props>(), { filled: undefined });
</script>

<template>
  <div v-if="filled !== null && filled !== undefined">
    <rating :filled="filled" />
  </div>
  <div v-else>
    <rating :filled="0" />
  </div>
</template>
