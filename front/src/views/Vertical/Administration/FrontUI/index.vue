<template>
  <div class="lg:w-2/3 mt-4 mx-auto flex flex-col">
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
