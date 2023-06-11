<template>
  <div class="w-screen h-app">
    <canvas
      class="w-full h-full outline-none"
      ref="iCanvas"
      tabindex="0"
      @mousemove="move"
      @mouseup="endMove"
      @mousedown="startMove"
      @wheel="zoom" />
  </div>
  <div class="fixed left-0 bottom-0 m-4">
    <svg
      class="cursor-pointer hover:opacity-50"
      @click="back"
      xmlns="http://www.w3.org/2000/svg"
      height="48px"
      viewBox="0 0 24 24"
      width="48px"
      fill="#ffffff">
      <path d="M0 0h24v24H0V0z" fill="none" />
      <path
        d="M12.5 8c-2.65 0-5.05.99-6.9 2.6L2 7v9h9l-3.62-3.62c1.39-1.16 3.16-1.88 5.12-1.88 3.54 0 6.55 2.31 7.6 5.5l2.37-.78C21.08 11.03 17.15 8 12.5 8z" />
    </svg>
  </div>
  <div class="flex flex-col fixed right-0 bottom-0 m-4">
    <div class="flex mx-auto text-white" v-if="state.current !== undefined">
      <span>{{ state.current + 1 }} / {{ state.imgs.length }}</span>
    </div>
    <div class="flex">
      <svg
        class="cursor-pointer hover:opacity-50"
        @click="previousPage"
        xmlns="http://www.w3.org/2000/svg"
        height="48px"
        viewBox="0 0 24 24"
        width="48px"
        fill="#ffffff">
        <path d="M0 0h24v24H0V0z" fill="none" />
        <path d="M15.61 7.41L14.2 6l-6 6 6 6 1.41-1.41L11.03 12l4.58-4.59z" />
      </svg>
      <svg
        class="cursor-pointer hover:opacity-50"
        @click="startPlay"
        v-if="!state.isPlay"
        xmlns="http://www.w3.org/2000/svg"
        height="48px"
        viewBox="0 0 24 24"
        width="48px"
        fill="#FFFFFF">
        <path d="M0 0h24v24H0V0z" fill="none" />
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z" />
      </svg>
      <svg
        class="cursor-pointer hover:opacity-50"
        @click="stopPlay"
        v-else
        xmlns="http://www.w3.org/2000/svg"
        height="48px"
        viewBox="0 0 24 24"
        width="48px"
        fill="#FFFFFF">
        <path
          d="M12,2C6.48,2,2,6.48,2,12s4.48,10,10,10s10-4.48,10-10S17.52,2,12,2z M11,16H9V8h2V16z M15,16h-2V8h2V16z" />
      </svg>
      <svg
        class="cursor-pointer hover:opacity-50"
        @click="nextPage"
        xmlns="http://www.w3.org/2000/svg"
        height="48px"
        viewBox="0 0 24 24"
        width="48px"
        fill="#ffffff">
        <path d="M0 0h24v24H0V0z" fill="none" />
        <path d="M10.02 6L8.61 7.41 13.19 12l-4.58 4.59L10.02 18l6-6-6-6z" />
      </svg>
    </div>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { ref, reactive, onMounted, onBeforeMount } from "vue";

import { getImages } from "@/api/v1/gallery/image";

export default {
  setup() {
    const route = useRoute();
    const gallery = route.params.gallery;
    const img_name = route.params.img;
    const timeInterval = route.query.interval ? parseInt(route.query.interval) : 5;

    const img = reactive(new Image());

    const state = reactive({
      imgs: [],
      current: undefined,
      isPlay: route.query.play,
      play: undefined,
    });

    getImages(gallery).then((response) => {
      state.imgs = response.data;
      state.current = state.imgs.indexOf(img_name);
    });

    let iCanvas = ref(null);

    const canvasStatus = reactive({
      xOffset: undefined,
      yOffset: undefined,
      xCursorStarted: undefined,
      yCursorStarted: undefined,
      initWidth: undefined,
      initHeight: undefined,
      width: undefined,
      height: undefined,
      draggable: false,
      scale: 1,
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
      state.play = setInterval(() => {
        const url = `${getNextPageUrl()}?play=1&interval=${timeInterval.toString()}`;
        window.open(url, "_self");
      }, timeInterval * 1000);
    }

    function stopPlay() {
      clearTimeout(state.play);
      state.isPlay = false;
    }

    function resize() {
      let slope = img.height / img.width;

      let canvasHeight = iCanvas.value.clientHeight;
      let canvasWidth = iCanvas.value.clientWidth;
      let canvasSlope = canvasHeight / canvasWidth;

      iCanvas.value.setAttribute("width", canvasWidth);
      iCanvas.value.setAttribute("height", canvasHeight);

      if (slope >= canvasSlope) {
        canvasStatus.height = canvasStatus.initHeight = canvasHeight;
        canvasStatus.width = canvasStatus.initWidth = canvasStatus.height / slope;
      } else {
        canvasStatus.height = canvasStatus.initHeight = canvasWidth * slope;
        canvasStatus.width = canvasStatus.initWidth = canvasWidth;
      }
      canvasStatus.xOffset = canvasStatus.width < canvasWidth ? (canvasWidth - canvasStatus.width) / 2 : 0;
      canvasStatus.yOffset = canvasStatus.height < canvasHeight ? (canvasHeight - canvasStatus.height) / 2 : 0;
      let ctx = iCanvas.value.getContext("2d");
      ctx.drawImage(img, canvasStatus.xOffset, canvasStatus.yOffset, canvasStatus.width, canvasStatus.height);
    }

    function load() {
      img.src = `/api/v1/gallery/${gallery}/${img_name}`;

      img.onload = resize;
    }

    onBeforeMount(() => {
      document.addEventListener.call(window, "keyup", (event) => {
        if (event.keyCode === 39) {
          nextPage();
        } else if (event.keyCode === 37) {
          previousPage();
        }
      });
      document.addEventListener.call(window, "resize", (event) => {
        resize();
      });
    });

    onMounted(() => {
      load();

      if (state.isPlay) {
        startPlay();
      }
    });

    function getPosition(event) {
      let canvas = event.target;
      let rect = canvas.getBoundingClientRect();
      let scaleX = canvas.width / rect.width;
      let scaleY = canvas.height / rect.height;
      let x = (event.clientX - rect.left) * scaleX;
      let y = (event.clientY - rect.top) * scaleY;
      return [x, y];
    }

    function startMove(event) {
      let pos = getPosition(event);
      canvasStatus.xCursorStarted = pos[0];
      canvasStatus.yCursorStarted = pos[1];
      canvasStatus.draggable = true;
    }

    function endMove() {
      canvasStatus.draggable = false;
    }

    function move(event) {
      if (canvasStatus.draggable) {
        let pos = getPosition(event);
        canvasStatus.xOffset += pos[0] - canvasStatus.xCursorStarted;
        canvasStatus.yOffset += pos[1] - canvasStatus.yCursorStarted;

        let ctx = iCanvas.value.getContext("2d");
        ctx.clearRect(0, 0, iCanvas.value.clientWidth, iCanvas.value.clientHeight);
        ctx.drawImage(img, canvasStatus.xOffset, canvasStatus.yOffset, canvasStatus.width, canvasStatus.height);

        canvasStatus.xCursorStarted = pos[0];
        canvasStatus.yCursorStarted = pos[1];
      }
    }

    function zoom(event) {
      let ctx = iCanvas.value.getContext("2d");

      if (event.deltaY > 0) {
        canvasStatus.scale *= 0.9;
      } else if (event.deltaY < 0) {
        canvasStatus.scale *= 1.1;
      }

      let lastWidth = canvasStatus.width;
      let lastHeight = canvasStatus.height;
      canvasStatus.width = canvasStatus.initWidth * canvasStatus.scale;
      canvasStatus.height = canvasStatus.initHeight * canvasStatus.scale;
      let lastScale = canvasStatus.width / lastWidth;

      let currentPos = getPosition(event);

      let relativeX = (currentPos[0] - iCanvas.value.clientWidth / 2) * (1 - lastScale);
      let relativeY = (currentPos[1] - iCanvas.value.clientHeight / 2) * (1 - lastScale);
      // console.log(relativeX, relativeY)

      // canvasStatus.xOffset -= (canvasStatus.width - lastWidth) / 2
      // canvasStatus.yOffset -= (canvasStatus.height - lastHeight) / 2
      canvasStatus.xOffset -= (canvasStatus.width - lastWidth) / 2;
      canvasStatus.yOffset -= (canvasStatus.height - lastHeight) / 2;
      ctx.clearRect(0, 0, iCanvas.value.clientWidth, iCanvas.value.clientHeight);
      ctx.drawImage(img, canvasStatus.xOffset, canvasStatus.yOffset, canvasStatus.width, canvasStatus.height);
    }

    return {
      state,
      iCanvas,
      move,
      startMove,
      endMove,
      zoom,
      startPlay,
      stopPlay,
      back,
      previousPage,
      nextPage,
    };
  },
};
</script>
