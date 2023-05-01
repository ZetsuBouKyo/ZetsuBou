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
      { title: "User", link: "/administration/user", active: false },
      { title: "Group", link: "/administration/group", active: false },
      { title: "Storage", link: "/administration/storage", active: false },
      { title: "Front UI", link: "/administration/front-ui", active: false },
      { title: "Task", link: "/administration/task", active: false },
    ];
    return { tabs };
  },
};
</script>
