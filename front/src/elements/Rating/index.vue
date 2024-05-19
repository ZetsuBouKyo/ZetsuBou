<script setup lang="ts">
import BaseRating from "./Base.vue";

interface Props {
  filled: number;
}
withDefaults(defineProps<Props>(), { filled: undefined });
</script>

<template>
  <div v-if="filled !== null && filled !== undefined">
    <base-rating :filled="filled" />
  </div>
  <div v-else>
    <base-rating :filled="0" />
  </div>
</template>
