<template>
  <div class="min-h-app">
    <div class="flex pt-4 bg-gray-900 sticky top-20 z-40">
      <tab class="w-2/3" :tabs="tabs" />
    </div>
    <router-view />
  </div>
</template>

<script>
import Tab from "@/elements/Tab/index.vue";

export default {
  components: { Tab },
  setup() {
    const tabs = [
      { title: "Quest", link: "/quest/quest", active: false },
      { title: "Elastic Count Quest", link: "/quest/elastic-count-quest", active: false },
    ];

    return { tabs };
  },
};
</script>
