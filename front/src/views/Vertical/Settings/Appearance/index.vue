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
            :placeholder="userState.frontSetting.gallery_preview_size" />
        </div>
        <div class="views-setting-row">
          <div class="views-setting-cell w-64">Image preview size:</div>
          <input class="views-setting-cell w-72" type="text" :placeholder="userState.frontSetting.img_preview_size" />
        </div>
        <div class="views-setting-row">
          <div class="views-setting-cell w-64">Autoplay Interval (seconds):</div>
          <input
            class="views-setting-cell w-72"
            type="text"
            :placeholder="userState.frontSetting.auto_play_time_interval" />
        </div>
      </div>
    </div>
    <div class="views-setting-section">
      <span class="views-setting-section-title">Video</span>
      <div class="views-setting-rows">
        <div class="views-setting-row">
          <div class="views-setting-cell w-56">Preview size:</div>
          <input class="views-setting-cell w-72" type="text" :placeholder="userState.frontSetting.video_preview_size" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { userState } from "@/state/user";

export default {
  setup() {
    return { userState };
  },
};
</script>
