<script setup lang="ts">
import { reactive } from "vue";

import { UserFrontSettings } from "@/interface/user";

import { putUserFrontSettings } from "@/api/v1/user/user";

import { messageState } from "@/state/message";
import { userState } from "@/state/user";

import { isPositiveInteger } from "@/utils/number";

enum SettingsType {
  PositiveInteger = "positiveinteger",
}

interface UserFrontSettingsPut extends UserFrontSettings {
  user_id: number;
}

interface PrivateState {
  data: UserFrontSettingsPut;
}

const privateState = reactive<PrivateState>({
  data: {
    user_id: userState.data.id,
    gallery_image_auto_play_time_interval: null,
    gallery_image_preview_size: null,
    gallery_preview_size: null,
    video_preview_size: null,
  },
});

const settings = [
  {
    key: "gallery_image_auto_play_time_interval",
    type: SettingsType.PositiveInteger,
    errorMessage: "Should be positive integer.",
  },
  {
    key: "gallery_image_preview_size",
    type: SettingsType.PositiveInteger,
    errorMessage: "Should be positive integer.",
  },
  {
    key: "gallery_preview_size",
    type: SettingsType.PositiveInteger,
    errorMessage: "Should be positive integer.",
  },
  {
    key: "video_preview_size",
    type: SettingsType.PositiveInteger,
    errorMessage: "Should be positive integer.",
  },
];

function save() {
  for (const s of settings) {
    const val = privateState.data[s.key];
    if (val === null) {
      continue;
    }
    if (!isPositiveInteger(val)) {
      messageState.push(s.errorMessage);
      return;
    }
  }

  putUserFrontSettings(userState.data.id, privateState.data).then((response) => {
    if (response.status === 200) {
      messageState.push("Saved");
    }
  });
}
</script>

<template>
  <div class="views-setting-container">
    <div class="views-setting-section">
      <span class="views-setting-section-title">Gallery</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <div class="views-setting-cell w-64">Preview size:</div>
          <input
            class="views-setting-cell w-72"
            type="text"
            :placeholder="userState.data.frontSettings.gallery_preview_size"
            v-model="privateState.data.gallery_preview_size" />
        </div>
        <div class="views-setting-row">
          <div class="views-setting-cell w-64">Image preview size:</div>
          <input
            class="views-setting-cell w-72"
            type="text"
            :placeholder="userState.data.frontSettings.gallery_image_preview_size"
            v-model="privateState.data.gallery_image_preview_size" />
        </div>
        <div class="views-setting-row">
          <div class="views-setting-cell w-64">Autoplay Interval (seconds):</div>
          <input
            class="views-setting-cell w-72"
            type="text"
            :placeholder="userState.data.frontSettings.gallery_image_auto_play_time_interval"
            v-model="privateState.data.gallery_image_auto_play_time_interval" />
        </div>
      </div>
    </div>
    <div class="views-setting-section">
      <span class="views-setting-section-title">Video</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <div class="views-setting-cell w-56">Preview size:</div>
          <input
            class="views-setting-cell w-72"
            type="text"
            :placeholder="userState.data.frontSettings.video_preview_size"
            v-model="privateState.data.video_preview_size" />
        </div>
        <div class="views-setting-row">
          <ripple-button class="flex btn btn-primary ml-auto" @click="save">Save</ripple-button>
        </div>
      </div>
    </div>
  </div>
</template>
