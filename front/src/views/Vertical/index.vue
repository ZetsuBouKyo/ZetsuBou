<script setup lang="ts">
import TopNav from "@/components/TopNav/index.vue";
import Message from "./Message.vue";
</script>

<template>
  <top-nav class="z-50" />
  <router-view class="text-gray-300" />
  <message />
</template>
