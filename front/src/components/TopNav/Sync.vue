<template>
  <confirm-modal
    ref="confirmNew"
    :title="'Warning'"
    :message="'Do you really want to synchronize new galleries?'"
    :on-close="onCloseConfirm"
    :on-confirm="onConfirmSynchronizeNew"
  />
  <confirm-modal
    ref="confirmAll"
    :title="'Warning'"
    :message="'Do you really want to synchronize all galleries?'"
    :on-close="onCloseConfirm"
    :on-confirm="onConfirmSynchronizeAll"
  />
  <div class="relative mx-1 h-10">
    <dropdown class="text-white border-2 border-gray-700 hover:bg-gray-600 rounded-lg">
      <template v-slot:select>
        <ripple-button
          class="focus:outline-none h-full"
          :title="state.action === 'new' ? 'synchronize new' : 'synchronize all'"
        >
          <div class="inline-flex items-center" @click="synchronize">
            <!-- <icon-ic-twotone-sync
              class="m-2"
              :class="state.isSync ? 'animate-spin' : ''"
              style="font-size: 1.2rem; color: white"
            /> -->
            <span class="mx-4 my-auto">Sync</span>
          </div>
        </ripple-button>
      </template>
      <template v-slot:options>
        <div class="flex flex-row ml-1 my-1">
          <span class="flex px-2 py-1 w-16 self-center">Query</span>
          <select
            class="flex py-1 px-2 ml-auto mr-1 bg-gray-800 border-gray-700 w-36 self-center"
            v-model="state.action"
          >
            <option class="my-1 mx-2" value="all">All</option>
            <option class="my-1 mx-2" value="new">New</option>
          </select>
        </div>
      </template>
    </dropdown>
  </div>
</template>

<script>
import { reactive, ref } from "vue";

import { getTaskStandaloneSyncNewGalleries } from "@/api/v1/task/standalone";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Dropdown from "@/elements/Dropdown/Dropdown.vue";
import ConfirmModal from "@/elements/Modal/ConfirmModal.vue";

export default {
  components: { RippleButton, Dropdown, ConfirmModal },
  setup() {
    const state = reactive({
      isSync: false,
      action: "new",
      sync: undefined,
    });

    const confirmNew = ref();
    const confirmAll = ref();
    function onCloseConfirm() {
      state.isSync = false;
    }

    function synchronize() {
      if (state.isSync) {
        return;
      }
      state.isSync = true;
      if (state.action === "new") {
        confirmNew.value.open();
      } else if (state.action === "all") {
        confirmAll.value.open();
      }
    }

    function onConfirmSynchronizeNew() {
      getTaskStandaloneSyncNewGalleries().then((response) => {
        if (response.status === 200) {
        }
      });
    }

    function onConfirmSynchronizeAll() {}

    return {
      state,
      confirmNew,
      onConfirmSynchronizeNew,
      confirmAll,
      onConfirmSynchronizeAll,
      onCloseConfirm,
      synchronize,
    };
  },
};
</script>
