<template>
  <div class="layout-container">
    <div class="flex"></div>
    <div class="flex flex-row">
      <div class="flex flex-col w-1/6 divide-y divide-gray-500">
        <slot></slot>
      </div>
      <div class="flex w-full">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import SettingAction from "./SettingAction.vue";
import SettingActionDropdown from "./SettingActionDropdown.vue";

export default {
  components: { SettingAction, SettingActionDropdown },
};
</script>
