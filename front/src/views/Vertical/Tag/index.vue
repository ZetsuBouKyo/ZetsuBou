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
      { title: "Tag", link: "/tag/tag", active: false },
      { title: "Token", link: "/tag/token", active: false },
      { title: "Attribute", link: "/tag/attribute", active: false },
    ];

    return { tabs };
  },
};
</script>
