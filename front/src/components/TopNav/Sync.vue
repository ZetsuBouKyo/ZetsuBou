<template>
  <confirm-modal
    ref="confirmNew"
    v-if="state.appMode !== undefined"
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
        <ripple-button class="focus:outline-none h-full">
          <div class="inline-flex items-center" @click="synchronize">
            <icon-ic-twotone-sync
              class="m-2"
              :class="state.isSync ? 'animate-spin' : ''"
              style="font-size: 1.2rem; color: white"
            />
            <span class="mr-4 my-auto">Sync</span>
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
            <option class="my-1 mx-2" value="new" v-if="state.appMode === SettingAppMode.Standalone">New</option>
          </select>
        </div>
      </template>
    </dropdown>
  </div>
</template>

<script lang="ts">
import { reactive, ref, watch, onBeforeMount } from "vue";
import { AxiosResponse } from "axios";

import {
  getTaskStandaloneSyncNewGalleries,
  getTaskStandaloneSyncNewProgress,
  deleteTaskStandaloneSyncNewProgress,
} from "@/api/v1/task/standalone";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Dropdown from "@/elements/Dropdown/Dropdown.vue";
import ConfirmModal from "@/elements/Modal/ConfirmModal.vue";

import { settingState, SettingAppMode } from "@/state/setting";

enum SyncMode {
  All = "all",
  New = "new",
}

export default {
  components: { RippleButton, Dropdown, ConfirmModal },
  setup() {
    const state = reactive({
      appMode: undefined,
      isSync: false,
      action: undefined,
      sync: undefined,
    });

    function load() {
      if (settingState.setting === undefined) {
        return;
      }
      state.appMode = settingState.setting.app_mode;
      switch (settingState.setting.app_mode) {
        case SettingAppMode.Standalone:
          state.action = SyncMode.New;
          break;
        case SettingAppMode.Cluster:
          state.action = SyncMode.All;
      }
    }
    load();
    watch(
      () => {
        if (settingState.setting !== undefined) {
          return settingState.setting.app_mode;
        }
        return undefined;
      },
      () => {
        load();
      },
    );

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
      switch (state.action) {
        case SyncMode.New:
          confirmNew.value.open();
          break;
        case SyncMode.All:
          confirmAll.value.open();
          break;
      }
    }

    async function synchronizeHandler(handler: any) {
      checkSyncState();
      return handler()
        .then((response: AxiosResponse) => {
          if (response.status === 200) {
            deleteProgress();
          }
        })
        .catch(() => {
          // console.log(error);
          state.isSync = false;
        });
    }

    function onConfirmSynchronizeNew() {
      synchronizeHandler(getTaskStandaloneSyncNewGalleries);
    }

    function onConfirmSynchronizeAll() {
      // synchronizeHandler(getTaskGallerySyncAll);
    }

    function deleteProgress() {
      deleteTaskStandaloneSyncNewProgress().then((response: AxiosResponse) => {
        if (response.status === 200) {
          clearTimeout(state.sync);
          state.isSync = false;
        }
      });
    }

    function getProgress() {
      getTaskStandaloneSyncNewProgress().then((response) => {
        if (response.status === 200) {
          if (response.data.progress_id === null) {
            clearTimeout(state.sync);
            state.isSync = false;
          } else if (response.data.progress === 100) {
            deleteProgress();
          }
        }
      });
    }

    function checkSyncState() {
      state.isSync = true;
      state.sync = setInterval(() => {
        getProgress();
      }, 1000);
    }

    getProgress();

    return {
      state,
      confirmNew,
      SyncMode,
      SettingAppMode,
      onConfirmSynchronizeNew,
      confirmAll,
      onConfirmSynchronizeAll,
      onCloseConfirm,
      synchronize,
    };
  },
};
</script>
