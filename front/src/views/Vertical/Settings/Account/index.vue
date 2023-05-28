<template>
  <modal ref="changeUser" :title="'Confirm'" class="w-1/3 top-1/4 left-1/3" :on-close="resetPassword">
    <div class="modal-row">
      <span class="w-32 mr-4">Password:</span>
      <form class="w-full">
        <input
          class="flex-1 modal-input w-full"
          type="password"
          autocomplete="new-password"
          v-model="userState.password"
        />
      </form>
    </div>
    <div class="modal-row">
      <div class="flex ml-auto">
        <ripple-button class="flex mr-2 btn btn-primary" @click="closeChangeUser"> Cancel </ripple-button>
        <ripple-button class="flex btn btn-danger" @click="confirmChangeUser"> Save </ripple-button>
      </div>
    </div>
  </modal>
  <div class="views-setting-container">
    <span class="views-setting-section-title">Account</span>
    <div class="views-setting-sections">
      <div class="views-setting-row">
        <div class="views-setting-cell">Name:</div>
        <input
          class="w-72 border-2 border-gray-600 text-white placeholder-gray-400 ml-4 px-4 rounded-lg focus:outline-none hidden sm:inline-block"
          :class="state.isNameEditable ? 'bg-gray-500' : 'bg-gray-600'"
          type="text"
          v-model="userState.newName"
          :placeholder="userState.name"
          :disabled="!state.isNameEditable"
        />
        <ripple-button
          class="flex btn btn-primary h-full mx-2 rounded-lg bg-blue-500 hover:opacity-50 hover:bg-gray-500 items-center"
          @click="makeNameEditable"
        >
          <icon-ic-outline-edit style="font-size: 1.2rem; color: white" />
        </ripple-button>
      </div>
      <div class="views-setting-row">
        <div class="views-setting-cell">Email:</div>
        <div class="views-setting-cell ml-4">{{ userState.email }}</div>
      </div>
      <div class="views-setting-row">
        <ripple-button class="flex btn btn-primary ml-auto" @click="openChangeUser">Save</ripple-button>
      </div>
      <div class="views-setting-section">
        <span class="views-setting-section-title">Change password</span>
        <div class="views-setting-sections">
          <div class="views-setting-row">
            <div class="views-setting-cell w-48">Old password:</div>
            <form>
              <input
                class="w-72 border-2 border-gray-600 bg-gray-500 text-white placeholder-gray-400 ml-4 px-4 rounded-lg focus:outline-none hidden sm:inline-block"
                type="password"
                autocomplete="new-password"
                v-model="userState.oldPassword"
              />
            </form>
          </div>
          <div class="views-setting-row">
            <div class="views-setting-cell w-48">New password:</div>
            <input
              class="w-72 border-2 border-gray-600 bg-gray-500 text-white placeholder-gray-400 ml-4 px-4 rounded-lg focus:outline-none hidden sm:inline-block"
              type="password"
              autocomplete="new-password"
              v-model="userState.newPassword"
            />
          </div>
          <div class="views-setting-row">
            <div class="views-setting-cell w-48">Confirm new password:</div>
            <input
              class="w-72 border-2 border-gray-600 bg-gray-500 text-white placeholder-gray-400 ml-4 px-4 rounded-lg focus:outline-none hidden sm:inline-block"
              type="password"
              autocomplete="new-password"
              v-model="userState.passwordConfirmation"
            />
          </div>
          <div class="views-setting-row">
            <ripple-button class="flex btn btn-primary ml-auto" @click="confirmChangeUser">Save</ripple-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { reactive, ref } from "vue";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Modal from "@/elements/Modal/Modal.vue";

import { userState } from "@/state/user";

export default {
  components: { RippleButton, Modal },
  setup() {
    const state = reactive({
      isNameEditable: false,
    });

    const changeUser = ref();

    function makeNameEditable() {
      state.isNameEditable = true;
    }

    function resetPassword() {
      userState.password = undefined;
    }

    function confirmChangeUser() {
      userState.update();
      changeUser.value.close();
    }

    function openChangeUser() {
      changeUser.value.open();
    }

    function closeChangeUser() {
      changeUser.value.close();
      resetPassword();
    }

    return {
      changeUser,
      closeChangeUser,
      confirmChangeUser,
      makeNameEditable,
      openChangeUser,
      resetPassword,
      state,
      userState,
    };
  },
};
</script>
