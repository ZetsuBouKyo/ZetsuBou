<script setup lang="ts">
import { PropType } from "vue";

import { GalleryImageState, GalleryImageSideBarEnum } from "../state.inferface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SlidebarIcon from "./SlidebarIcon.vue";

const props = defineProps({
  state: {
    type: Object as PropType<GalleryImageState>,
    required: true,
  },
});

const state = props.state;

function select() {
  state.layers.isEdit = false;
}

function edit() {
  state.layers.isEdit = true;
}

function toggleGrid() {
  state.sidebar.isGrid = !state.sidebar.isGrid;
}

function rotateRight() {
  state.container.rotation += 1;
}

function rotateLeft() {
  state.container.rotation -= 1;
}

function rulerPlus1() {
  state.container.gridStep += 1;
}

function rulerMinus1() {
  state.container.gridStep -= 1;
}

function reset() {
  state.container.gridAlpha = state.container.defaultGridAlpha;
  state.container.gridLineWidth = state.container.defaultGridLineWidth;
  state.container.gridStep = state.container.defaultGridStep;
  state.container.originX = state.container.defaultOriginX;
  state.container.originY = state.container.defaultOriginY;
  state.container.rotation = state.container.defaultRotation;
  state.container.scale = state.container.defaultScale;
}

function changeCategory(category: GalleryImageSideBarEnum) {
  switch (category) {
    case GalleryImageSideBarEnum.Cursor:
      state.sidebar.isSubSidebar = false;
      break;
    case GalleryImageSideBarEnum.Grid:
    case GalleryImageSideBarEnum.Rotation:
      if (category === state.sidebar.category) {
        state.sidebar.isSubSidebar = !state.sidebar.isSubSidebar;
      } else {
        state.sidebar.isSubSidebar = true;
      }
      break;
  }

  state.sidebar.category = category;
}

function openCursor() {
  changeCategory(GalleryImageSideBarEnum.Cursor);
}

function openRotation() {
  changeCategory(GalleryImageSideBarEnum.Rotation);
}

function updateRotation() {
  state.container.rotation += Number(state.sidebar.rotation.degree);
  state.container.rotation = state.container.rotation % 360;
}

function openGrid() {
  changeCategory(GalleryImageSideBarEnum.Grid);
}

function updateGridStep() {
  if (state.sidebar.grid.alpha !== undefined) {
    state.container.gridAlpha = Number(state.sidebar.grid.alpha);
  }
  if (state.sidebar.grid.lineWidth !== undefined) {
    state.container.gridLineWidth = Number(state.sidebar.grid.lineWidth);
  }
  if (state.sidebar.grid.step !== undefined) {
    state.container.gridStep = Number(state.sidebar.grid.step);
  }
}
</script>

<template>
  <div class="h-app bg-gray-900 flex flex-row items-center">
    <div class="h-full flex flex-col overflow-y-scroll scrollbar-gray-100-2">
      <slidebar-icon class="mt-4">
        <icon-entypo-save style="font-size: 1.5rem; color: white" />
      </slidebar-icon>
      <slidebar-icon
        :class="state.sidebar.category === GalleryImageSideBarEnum.Cursor ? 'bg-indigo-500 rounded-lg' : ''"
        @click="openCursor">
        <icon-clarity-cursor-arrow-solid style="font-size: 1.5rem; color: white" @click="select" />
      </slidebar-icon>
      <slidebar-icon
        :class="state.sidebar.category === GalleryImageSideBarEnum.Polygon ? 'bg-indigo-500 rounded-lg' : ''">
        <icon-mdi-vector-polygon style="font-size: 1.5rem; color: white" @click="edit" />
      </slidebar-icon>
      <slidebar-icon>
        <icon-ion-ios-pricetags style="font-size: 1.5rem; color: white" />
      </slidebar-icon>
      <slidebar-icon>
        <icon-whh-layerorderup style="font-size: 1.5rem; color: white" />
      </slidebar-icon>
      <slidebar-icon>
        <icon-mdi-format-horizontal-align-center style="font-size: 1.5rem; color: white" @click="reset" />
      </slidebar-icon>
      <slidebar-icon
        :class="state.sidebar.category === GalleryImageSideBarEnum.Rotation ? 'bg-indigo-500 rounded-lg' : ''"
        @click="openRotation">
        <icon-mdi-arrow-oscillating style="font-size: 1.5rem; color: white" />
      </slidebar-icon>
      <slidebar-icon>
        <icon-mdi-rotate-right style="font-size: 1.5rem; color: white" @click="rotateRight" />
      </slidebar-icon>
      <slidebar-icon>
        <icon-mdi-rotate-left style="font-size: 1.5rem; color: white" @click="rotateLeft" />
      </slidebar-icon>
      <slidebar-icon
        :class="state.sidebar.category === GalleryImageSideBarEnum.Grid ? 'bg-indigo-500 rounded-lg' : ''"
        @click="openGrid">
        <icon-solar-ruler-pen-linear style="font-size: 1.5rem; color: white" />
      </slidebar-icon>
      <slidebar-icon :class="state.sidebar.isGrid ? 'bg-gray-500 rounded-lg' : ''">
        <icon-solar-ruler-angular-linear style="font-size: 1.5rem; color: white" @click="toggleGrid" />
      </slidebar-icon>
      <slidebar-icon>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 24 24"
          style="font-size: 1.5rem; color: white"
          @click="rulerPlus1">
          <path
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M15 5h3m3 0h-3m0 0V2m0 3v3m-7-1V2.6a.6.6 0 0 0-.6-.6H3.6a.6.6 0 0 0-.6.6v18.8a.6.6 0 0 0 .6.6h6.8a.6.6 0 0 0 .6-.6V17m0-10H8m3 0v5m0 0H8m3 0v5m0 0H8" />
        </svg>
      </slidebar-icon>
      <slidebar-icon>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 24 24"
          style="font-size: 1.5rem; color: white"
          @click="rulerMinus1">
          <path
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M15 5h6M11 7V2.6a.6.6 0 0 0-.6-.6H3.6a.6.6 0 0 0-.6.6v18.8a.6.6 0 0 0 .6.6h6.8a.6.6 0 0 0 .6-.6V17m0-10H8m3 0v5m0 0H8m3 0v5m0 0H8" />
        </svg>
      </slidebar-icon>
    </div>
    <div
      class="h-full w-72 flex bg-gray-700 text-white"
      :key="(state.sidebar.isSubSidebar, state.sidebar.category)"
      v-if="state.sidebar.isSubSidebar">
      <div
        class="h-full w-full flex flex-col overflow-y-scroll scrollbar-gray-100-2"
        :key="(state.sidebar.isSubSidebar, GalleryImageSideBarEnum.Grid)"
        v-if="state.sidebar.category === GalleryImageSideBarEnum.Grid">
        <div class="flex flex-col">
          <span class="modal-row-10">Current alpha: {{ state.container.gridAlpha }}</span>
        </div>
        <div class="flex flex-col">
          <span class="modal-row-10">Current line width: {{ state.container.gridLineWidth }}</span>
        </div>
        <div class="flex flex-col">
          <span class="modal-row-10">Current step: {{ state.container.gridStep }}</span>
        </div>
        <div class="flex flex-col">
          <span class="modal-row-10">Alpha:</span>
          <input class="modal-input-10" v-model="state.sidebar.grid.alpha" />
        </div>
        <div class="flex flex-col">
          <span class="modal-row-10">Line width:</span>
          <input class="modal-input-10" v-model="state.sidebar.grid.lineWidth" />
        </div>
        <div class="flex flex-col">
          <span class="modal-row-10">Step:</span>
          <input class="modal-input-10" v-model="state.sidebar.grid.step" />
        </div>
        <div class="flex flex-col">
          <div class="modal-row-10">
            <div class="flex ml-auto">
              <ripple-button class="flex btn btn-primary" @click="updateGridStep"> Update </ripple-button>
            </div>
          </div>
        </div>
      </div>
      <div
        class="h-full w-full flex flex-col overflow-y-scroll scrollbar-gray-100-2"
        :key="(state.sidebar.isSubSidebar, GalleryImageSideBarEnum.Rotation)"
        v-else-if="state.sidebar.category === GalleryImageSideBarEnum.Rotation">
        <div class="flex flex-col">
          <span class="modal-row-10">Current degree: {{ state.container.rotation }}°</span>
        </div>
        <div class="flex flex-col">
          <span class="modal-row-10">Add angle (degrees):</span>
          <input class="modal-input-10" v-model="state.sidebar.rotation.degree" placeholder="-360 ~ 360" />
          <div class="modal-row-10">
            <div class="flex ml-auto">
              <ripple-button class="flex btn btn-primary" @click="updateRotation"> Update </ripple-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
