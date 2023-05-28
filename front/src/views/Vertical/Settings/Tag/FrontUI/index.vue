<template>
  <div class="views-setting-container">
    <gallery-setting />
    <video-setting class="my-4" />
  </div>
</template>

<script lang="ts">
import GallerySetting from "./Gallery.vue";
import VideoSetting from "./Video.vue";

export default {
  components: { GallerySetting, VideoSetting },
};
</script>
