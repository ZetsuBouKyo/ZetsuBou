<script setup lang="ts">
import { onMounted, reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { GalleryImageState, GalleryImageSideBarEnum } from "./state.inferface";

import PlayPanel from "./PlayPanel.vue";
import Sidebar from "./Sidebar/index.vue";

import { detectRouteChange } from "@/utils/route";

const props = defineProps({});

const route = useRoute();

const state = reactive<GalleryImageState>({
  container: {
    gallery: route.params.gallery,
    imgName: route.params.img,
    imgUrl: undefined,
    imgWidth: undefined,
    imgHeight: undefined,
    defaultGridAlpha: 0.8,
    defaultGridLineWidth: 0.5,
    defaultGridStep: 20,
    defaultOriginX: 0,
    defaultOriginY: 0,
    defaultRotation: 0,
    defaultScale: 1,
    gridAlpha: 0.8,
    gridLineWidth: 0.5,
    gridStep: 20,
    originX: 0,
    originY: 0,
    rotation: 0,
    scale: 1,
    scaleFactor: 1.1,
    dragStart: null,
  },
  bookmark: {
    isBookmark: false,
  },
  sidebar: {
    isGrid: false,
    isSidebar: false,
    isSubSidebar: false,
    category: GalleryImageSideBarEnum.Cursor,
    grid: {
      alpha: undefined,
      lineWidth: undefined,
      step: undefined,
    },
    rotation: {
      degree: undefined,
    },
    activateSidebar: () => {
      state.sidebar.isSidebar = true;
    },
    closeSidebar: () => {
      state.sidebar.isSidebar = false;
    },
    toggleSidebar: () => {
      state.sidebar.isSidebar = !state.sidebar.isSidebar;
    },
  },
  panel: {
    imgs: [],
    galleryID: route.params.gallery as string,
    imgName: route.params.img as string,
    timeInterval: route.query.interval ? parseInt(route.query.interval as string) : 5,
    current: undefined,
    isPlay: route.query.play as any,
    play: undefined,
  },
  layers: {
    current: {
      layer: 0,
      selection: 0,
    },
    isEdit: false,
    layers: [],
  },
});

const canvas = ref(null);
const ctx = ref(null);
const image = new Image();

const resizeAndCenterImage = () => {
  const canvasAspectRatio = canvas.value.width / canvas.value.height;
  const imageAspectRatio = state.container.imgWidth / state.container.imgHeight;

  if (canvasAspectRatio > imageAspectRatio) {
    state.container.scale = canvas.value.height / state.container.imgHeight;
  } else {
    state.container.scale = canvas.value.width / state.container.imgWidth;
  }

  state.container.originX = (canvas.value.width - state.container.imgWidth * state.container.scale) / 2;
  state.container.originY = (canvas.value.height - state.container.imgHeight * state.container.scale) / 2;

  state.container.defaultScale = state.container.scale;
  state.container.defaultOriginX = state.container.originX;
  state.container.defaultOriginY = state.container.originY;
};

const drawGrid = () => {
  ctx.value.save();
  ctx.value.globalAlpha = state.container.gridAlpha;
  ctx.value.lineWidth = state.container.gridLineWidth;

  const step = state.container.gridStep;
  const width = canvas.value.width;
  const height = canvas.value.height;

  for (let x = 0; x < width; x += step) {
    ctx.value.beginPath();
    ctx.value.strokeStyle = "white";
    ctx.value.moveTo(x, 0);
    ctx.value.lineTo(x, height);
    ctx.value.stroke();

    const x2 = x + ctx.value.lineWidth;
    ctx.value.beginPath();
    ctx.value.strokeStyle = "black";
    ctx.value.moveTo(x2, 0);
    ctx.value.lineTo(x2, height);
    ctx.value.stroke();
  }

  for (let y = 0; y < height; y += step) {
    ctx.value.beginPath();
    ctx.value.strokeStyle = "white";
    ctx.value.moveTo(0, y);
    ctx.value.lineTo(width, y);
    ctx.value.stroke();

    const y2 = y + ctx.value.lineWidth;
    ctx.value.beginPath();
    ctx.value.strokeStyle = "black";
    ctx.value.moveTo(0, y2);
    ctx.value.lineTo(width, y2);
    ctx.value.stroke();
  }

  ctx.value.restore();
};

function drawPoint() {}

function drawPolygon(polygonPoints: Array<{ x: number; y: number }>) {
  if (polygonPoints.length > 1) {
    ctx.value.beginPath();
    ctx.value.strokeStyle = "red";
    ctx.value.lineWidth = 2 / state.container.scale;
    ctx.value.moveTo(polygonPoints[0].x, polygonPoints[0].y);
    for (let i = 1; i < polygonPoints.length; i++) {
      ctx.value.lineTo(polygonPoints[i].x, polygonPoints[i].y);
    }
    ctx.value.closePath();
    ctx.value.stroke();

    // Draw circles at each polygon point
    polygonPoints.forEach((point) => {
      ctx.value.beginPath();
      ctx.value.strokeStyle = "red";
      ctx.value.arc(point.x, point.y, 2 / state.container.scale, 0, 2 * Math.PI);
      ctx.value.stroke();
    });
  }
}

const draw = () => {
  if (!canvas.value || !ctx.value || state.container.imgWidth === undefined || state.container.imgHeight === undefined)
    return;

  ctx.value.save();
  ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
  ctx.value.translate(
    state.container.originX + (state.container.imgWidth * state.container.scale) / 2,
    state.container.originY + (state.container.imgHeight * state.container.scale) / 2,
  ); // Move to the center of the image
  ctx.value.rotate((Math.PI * state.container.rotation) / 360); // Apply rotation
  ctx.value.translate(
    (-state.container.imgWidth * state.container.scale) / 2,
    (-state.container.imgHeight * state.container.scale) / 2,
  ); // Move back to the top-left corner of the image
  ctx.value.scale(state.container.scale, state.container.scale);
  ctx.value.drawImage(image, 0, 0, state.container.imgWidth, state.container.imgHeight);

  const ImageRectangle = [
    { x: 0, y: state.container.imgHeight },
    { x: state.container.imgWidth, y: state.container.imgHeight },
    { x: state.container.imgWidth, y: 0 },
    { x: 0, y: 0 },
  ];
  drawPolygon(ImageRectangle);

  ctx.value.restore();
  if (state.sidebar.isGrid) {
    drawGrid();
  }
};

const zoom = (event: WheelEvent) => {
  event.preventDefault();
  const scaleFactor = state.container.scaleFactor;
  const mouseX = event.clientX - canvas.value.offsetLeft;
  const mouseY = event.clientY - canvas.value.offsetTop;
  const zoomIn = event.deltaY < 0;

  const newScale = zoomIn ? state.container.scale * scaleFactor : state.container.scale / scaleFactor;
  const zoomRatio = newScale / state.container.scale;

  // Adjust the origin to zoom around the cursor
  state.container.originX = mouseX - (mouseX - state.container.originX) * zoomRatio;
  state.container.originY = mouseY - (mouseY - state.container.originY) * zoomRatio;
  state.container.scale = newScale;
  draw();
};

const startDrag = (event: MouseEvent) => {
  state.container.dragStart = {
    x: event.clientX - state.container.originX,
    y: event.clientY - state.container.originY,
  };
};

const drag = (event: MouseEvent) => {
  if (state.container.dragStart) {
    state.container.originX = event.clientX - state.container.dragStart.x;
    state.container.originY = event.clientY - state.container.dragStart.y;
    draw();
  }
};

const endDrag = () => {
  state.container.dragStart = null;
};

function getImgUrl() {
  return `/api/v1/gallery/${state.container.gallery}/i/${state.container.imgName}`;
}

function load() {
  if (route.params.gallery === undefined || route.params.img === undefined) {
    return;
  }

  state.container.gallery = route.params.gallery;
  state.container.imgName = route.params.img;
  state.container.imgUrl = getImgUrl();

  image.src = state.container.imgUrl; // Provide the path to your image here

  image.onload = () => {
    state.container.imgWidth = image.width;
    state.container.imgHeight = image.height;
    resizeAndCenterImage();
    draw();
  };

  document.addEventListener.call(window, "resize", () => {
    loadCanvas();
    draw();
  });
  document.addEventListener.call(window, "keyup", (event) => {
    if (event.keyCode === 13) {
      state.container.rotation += Math.PI / 6;
      draw();
    }
  });
}
load();

watch(
  () => {
    return [detectRouteChange(route)];
  },
  () => {
    load();
  },
);

watch(
  () => {
    return [
      state.container.gridAlpha,
      state.container.gridLineWidth,
      state.container.gridStep,
      state.container.rotation,
      state.sidebar.isGrid,
    ];
  },
  () => {
    draw();
  },
);

function loadCanvas() {
  canvas.value.width = canvas.value.offsetWidth;
  canvas.value.height = canvas.value.offsetHeight;
  ctx.value = canvas.value.getContext("2d");
}

onMounted(() => {
  loadCanvas();
  draw();
});
</script>

<template>
  <div class="h-app w-full">
    <canvas
      class="h-app w-full"
      ref="canvas"
      @click="drawPoint"
      @mousedown="startDrag"
      @mousemove="drag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
      @wheel="zoom"></canvas>
  </div>
  <sidebar class="animate-slide-in fixed top-20 left-0" :state="state" v-if="state.sidebar.isSidebar" />
  <play-panel :svg="state" />
</template>
