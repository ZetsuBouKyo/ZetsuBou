<template>
  <main>
    <router-view class="text-gray-400" />
  </main>
</template>

<script>
import TopNav from "@/components/TopNav/index.vue";

export default {
  components: { TopNav },
};
</script>
