<template>
  <confirm-modal
    ref="confirmNew"
    v-if="state.appMode !== undefined"
    :title="'Warning'"
    :message="'Do you really want to synchronize new galleries?'"
    :on-close="onCloseConfirm"
    :on-confirm="onConfirmSynchronizeNew" />
  <confirm-modal
    ref="confirmAll"
    :title="'Warning'"
    :message="'Do you really want to synchronize all galleries?'"
    :on-close="onCloseConfirm"
    :on-confirm="onConfirmSynchronizeAll" />
  <div class="relative mx-1 h-10">
    <dropdown class="text-white border-2 border-gray-700 hover:bg-gray-600 rounded-lg">
      <template v-slot:select>
        <ripple-button class="focus:outline-none h-full rounded-l-lg">
          <div class="flex flex-row my-auto" @click="synchronize">
            <svg class="mx-2" width="24" height="24" viewBox="0 0 24 24" style="transform: rotate(-90deg)">
              <circle cx="12" cy="12" r="10.8" fill="none" stroke="#e6e6e6" stroke-width="2.4" />
              <circle
                cx="12"
                cy="12"
                r="10.8"
                fill="none"
                stroke="#3b82f6"
                stroke-width="2.4"
                pathLength="100"
                style="stroke-dasharray: 100; stroke-dashoffset: 100; stroke-linecap: round"
                :style="'stroke-dashoffset:' + state.progress + ';'" />
            </svg>
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
            :disabled="state.isSync">
            <option class="my-1 mx-2" value="all">All</option>
            <option class="my-1 mx-2" value="new" v-if="state.appMode === AppModeEnum.Standalone">New</option>
          </select>
        </div>
      </template>
    </dropdown>
  </div>
</template>

<script lang="ts">
import { reactive, ref, watch } from "vue";
import { AxiosResponse } from "axios";

import {
  getTaskStandaloneSyncNewGalleries,
  getTaskStandaloneSyncNewProgress,
  deleteTaskStandaloneSyncNewProgress,
} from "@/api/v1/task/standalone";
import {
  postSyncStoragesMinio,
  getTaskAirflowSyncStoragesProgress,
  deleteTaskAirflowSyncStoragesProgress,
} from "@/api/v1/task/airflow";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Dropdown from "@/elements/Dropdown/Dropdown.vue";
import ConfirmModal from "@/elements/Modal/ConfirmModal.vue";

import { messageState } from "@/state/message";
import { settingState } from "@/state/setting";

import { AppModeEnum } from "@/interface/setting";

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
      syncAll: undefined,
      syncNew: undefined,
      progress: 100,
    });

    function load() {
      if (settingState.setting === undefined) {
        return;
      }
      state.appMode = settingState.setting.app_mode;
      switch (settingState.setting.app_mode) {
        case AppModeEnum.Standalone:
          state.action = SyncMode.New;
          break;
        case AppModeEnum.Cluster:
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
      switch (state.action) {
        case SyncMode.New:
          confirmNew.value.open();
          break;
        case SyncMode.All:
          confirmAll.value.open();
          break;
      }
    }

    async function synchronizeHandler(syncRequest: any, getProgressRequest: any, deleteProgressRequest: any) {
      state.isSync = true;
      checkSyncState(getProgressRequest, deleteProgressRequest);
      return syncRequest()
        .then((response: AxiosResponse) => {
          if (response.status === 200) {
          }
        })
        .catch(() => {
          // console.log(error);
          state.isSync = false;
        });
    }

    function onConfirmSynchronizeNew() {
      synchronizeHandler(
        getTaskStandaloneSyncNewGalleries,
        getTaskStandaloneSyncNewProgress,
        deleteTaskStandaloneSyncNewProgress,
      );
    }

    function onConfirmSynchronizeAll() {
      synchronizeHandler(
        postSyncStoragesMinio,
        getTaskAirflowSyncStoragesProgress,
        deleteTaskAirflowSyncStoragesProgress,
      );
    }

    function deleteInterval(action: SyncMode) {
      switch (action) {
        case SyncMode.All:
          clearInterval(state.syncAll);
          state.syncAll = undefined;
          break;
        case SyncMode.New:
          clearInterval(state.syncNew);
          state.syncNew = undefined;
          break;
      }
    }

    function deleteProgress(action: SyncMode, deleteRequest: any) {
      deleteRequest()
        .then((response: AxiosResponse) => {
          if (response.status === 200) {
            deleteInterval(action);
            state.isSync = false;
          }
        })
        .catch(() => {});
    }

    function getProgress(action: SyncMode, getRequest: any, deleteRequest: any) {
      getRequest()
        .then((response: any) => {
          if (response.status === 200) {
            switch (response.data.progress) {
              case null:
                if (!state.isSync) {
                  deleteInterval(action);
                }
                break;
              case 100:
                deleteProgress(action, deleteRequest);
                state.isSync = false;
                state.progress = 0;
                messageState.push("Successfully synchronized storages");
                break;
              default:
                state.isSync = true;
                state.progress = 100 - response.data.progress;
            }
          }
        })
        .catch(() => {
          deleteInterval(action);
        });
    }

    function checkSyncState(getProgressRequest: any, deleteProgressRequest: any) {
      switch (state.action) {
        case SyncMode.All:
          if (state.syncAll === undefined) {
            state.syncAll = setInterval(() => {
              getProgress(SyncMode.All, getProgressRequest, deleteProgressRequest);
            }, 2000);
          }
          break;
        case SyncMode.New:
          if (state.syncNew === undefined) {
            state.syncNew = setInterval(() => {
              getProgress(SyncMode.New, getProgressRequest, deleteProgressRequest);
            }, 2000);
          }
          break;
      }
    }

    function initSyncState() {
      switch (state.action) {
        case SyncMode.All:
          checkSyncState(getTaskAirflowSyncStoragesProgress, deleteTaskAirflowSyncStoragesProgress);
          break;
        case SyncMode.New:
          checkSyncState(getTaskStandaloneSyncNewProgress, deleteTaskStandaloneSyncNewProgress);
          break;
      }
    }
    initSyncState();
    watch(
      () => state.action,
      () => {
        state.progress = 100;
        deleteInterval(SyncMode.All);
        deleteInterval(SyncMode.New);
        initSyncState();
      },
    );

    return {
      state,
      confirmNew,
      SyncMode,
      AppModeEnum,
      onConfirmSynchronizeNew,
      confirmAll,
      onConfirmSynchronizeAll,
      onCloseConfirm,
      synchronize,
    };
  },
};
</script>
