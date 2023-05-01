<template>
  <div class="hidden sm:block fixed right-0 top-20 m-4 bg-opacity-50 rounded-lg p-2">
    <icon-mdi-file-edit-outline
      class="cursor-pointer hover:opacity-50 opacity-100"
      style="font-size: 1.5rem; color: white"
      @click="tagger.toggleTagger"
    />
  </div>
  <div class="fixed left-0 bottom-3 bg-opacity-50 rounded-lg m-2 flex">
    <icon-ri-arrow-go-back-fill
      class="cursor-pointer hover:opacity-50 opacity-100"
      style="font-size: 1.5rem; color: white"
      @click="back"
    />
  </div>
  <div class="flex flex-col fixed right-0 bottom-0 m-4 bg-gray-900 bg-opacity-50 rounded-lg p-2">
    <div class="flex mx-auto text-white" v-if="state.current !== undefined">
      <span>{{ state.current + 1 }} / {{ state.imgs.length }}</span>
    </div>
    <div class="flex">
      <icon-ic-round-keyboard-arrow-left
        class="cursor-pointer hover:opacity-50"
        style="font-size: 2rem; color: white"
        @click="previousPage"
      />
      <icon-ic-sharp-play-circle-filled
        class="cursor-pointer hover:opacity-50"
        style="font-size: 2rem; color: white"
        @click="startPlay"
        v-if="!state.isPlay"
      />
      <icon-ic-round-stop-circle
        class="cursor-pointer hover:opacity-50"
        style="font-size: 2rem; color: white"
        @click="stopPlay"
        v-else
      />
      <icon-ic-round-keyboard-arrow-right
        class="cursor-pointer hover:opacity-50"
        style="font-size: 2rem; color: white"
        @click="nextPage"
      />
    </div>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { reactive, onMounted, onBeforeMount } from "vue";

import { getImages } from "@/api/v1/gallery/image";

export default {
  props: {
    tagger: {
      type: Object,
      default: undefined,
    },
  },
  setup(props) {
    const tagger = props.tagger;
    const route = useRoute();
    const gallery = route.params.gallery;
    const imgName = route.params.img;
    const timeInterval = route.query.interval ? parseInt(route.query.interval) : 5;

    const state = reactive({
      imgs: [],
      current: undefined,
      isPlay: route.query.play,
      play: undefined,
    });

    function back() {
      const url = "/g/" + gallery;
      window.open(url, "_self");
    }

    function getNextPageUrl() {
      const nextP = state.current + 1;
      let url = undefined;
      if (nextP < state.imgs.length) {
        url = `/g/${gallery}/i/${state.imgs[nextP]}`;
      }
      return url;
    }

    function previousPage() {
      const previousP = state.current - 1;
      if (previousP > -1) {
        const url = `/g/${gallery}/i/${state.imgs[previousP]}`;
        window.open(url, "_self");
      }
    }

    function nextPage() {
      const url = getNextPageUrl();
      if (url !== undefined) {
        window.open(url, "_self");
      }
    }

    function startPlay() {
      state.isPlay = true;
      // console.log(state.current, state.imgs.length);
      if (state.current === state.imgs.length - 1) {
        state.isPlay = false;
        return;
      }
      state.play = setInterval(() => {
        const url = `${getNextPageUrl()}?play=1&interval=${timeInterval.toString()}`;
        window.open(url, "_self");
      }, timeInterval * 1000);
    }

    function stopPlay() {
      clearTimeout(state.play);
      state.isPlay = false;
    }

    onBeforeMount(() => {
      document.addEventListener.call(window, "keyup", (event) => {
        if (event.keyCode === 39) {
          nextPage();
        } else if (event.keyCode === 37) {
          previousPage();
        }
      });
    });

    onMounted(() => {
      getImages(gallery).then((response) => {
        state.imgs = response.data;
        state.current = state.imgs.indexOf(imgName);
        if (state.isPlay) {
          startPlay();
        }
      });
    });

    return {
      tagger,
      state,
      startPlay,
      stopPlay,
      back,
      previousPage,
      nextPage,
    };
  },
};
</script>
