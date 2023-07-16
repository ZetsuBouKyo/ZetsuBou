<script setup lang="ts">
import { reactive, ref } from "vue";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Dropdown from "@/elements/Dropdown/Dropdown.vue";
import QuestProgress from "./QuestProgress.vue";

import { userState } from "@/state/user";
import { progressState } from "./progress";

const dropdown = ref();

const dropdownState = reactive({
  popout: false,
  close: () => {
    dropdownState.popout = false;
  },
  activate: () => {
    dropdownState.popout = true;
  },
  toggle: () => {
    dropdownState.popout = !dropdownState.popout;
  },
});

function signOut() {
  userState.signOut();
  window.open("/", "_self");
}

progressState.init();

function close() {
  dropdown.value.close();
}
</script>

<template>
  <div class="relative mx-1">
    <dropdown
      ref="dropdown"
      class="text-white bg-gray-700 border-2 border-gray-600 hover:bg-gray-500 rounded-lg"
      :selectClass="'border-r-2 border-gray-600'">
      <template v-slot:select>
        <button class="focus:outline-none">
          <div
            class="inline-flex items-center h-full"
            :title="progressState.data.title ? progressState.data.title : undefined">
            <icon-ph-user-bold class="m-1 h-8" style="font-size: 1.4rem" />
            <div class="w-32 mr-2 hidden lg:flex lg:flex-col">
              <span class="text-left truncate" :class="progressState.data.style ? 'text-sm' : ''">{{
                userState.data.name
              }}</span>
              <quest-progress />
            </div>
          </div>
        </button>
      </template>
      <template v-slot:options>
        <ripple-button class="flex w-full">
          <router-link class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white" to="" @click="close">
            <icon-ic-baseline-person class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Profile</span>
          </router-link>
        </ripple-button>
        <ripple-button class="flex w-full">
          <router-link class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white" to="" @click="close">
            <icon-ic-outline-analytics class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Analytics</span>
          </router-link>
        </ripple-button>
        <ripple-button class="flex w-full">
          <router-link
            class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white"
            to="/bookmark/gallery"
            @click="close">
            <icon-mdi-bookmark-outline class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Bookmark</span>
          </router-link>
        </ripple-button>
        <ripple-button class="flex w-full">
          <router-link
            class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white"
            to="/settings/account"
            @click="close">
            <icon-mdi-user-settings-variant class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Settings</span>
          </router-link>
        </ripple-button>
        <ripple-button class="flex w-full focus:outline-none">
          <a class="flex flex-row p-2 w-full hover:bg-gray-600 hover:text-white" @click="signOut">
            <icon-octicon-sign-out class="self-center ml-2" style="font-size: 1.4rem" />
            <span class="flex px-2 py-1 self-center">Sign Out</span>
          </a>
        </ripple-button>
      </template>
    </dropdown>
  </div>
</template>
