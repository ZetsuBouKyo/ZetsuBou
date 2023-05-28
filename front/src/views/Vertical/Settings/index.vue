<template>
  <div class="flex flex-col w-2/3 mx-auto mt-4">
    <div class="flex"></div>
    <div class="flex flex-row">
      <div class="flex flex-col w-1/6">
        <ripple-button class="views-setting-action-ripple-button">
          <a class="views-setting-action" href="/settings/account">
            <icon-ic-baseline-person class="views-setting-action-icon" style="font-size: 1.4rem" />
            <span class="views-setting-action">Account</span>
          </a>
        </ripple-button>
        <ripple-button class="views-setting-action-ripple-button">
          <a class="views-setting-action" href="/settings/appearance">
            <icon-ic-outline-edit class="views-setting-action-icon" style="font-size: 1.4rem" />
            <span class="views-setting-action">Appearance</span>
          </a>
        </ripple-button>
        <ripple-button class="views-setting-action-ripple-button">
          <a class="views-setting-action" href="/settings/authentication">
            <icon-ic-outline-edit class="views-setting-action-icon" style="font-size: 1.4rem" />
            <span class="views-setting-action">Authentication</span>
          </a>
        </ripple-button>
      </div>
      <div class="flex w-full">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import RippleButton from "@/elements/Button/RippleButton.vue";

export default {
  components: { RippleButton },
  setup() {
    return {};
  },
};
</script>
