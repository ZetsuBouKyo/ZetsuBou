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

function toggleRuler() {
  state.sidebar.isRuler = !state.sidebar.isRuler;
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
    case GalleryImageSideBarEnum.Rotation:
      state.sidebar.isSubSidebar = !state.sidebar.isSubSidebar;
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
      <slidebar-icon :class="state.sidebar.isRuler ? 'bg-gray-500 rounded-lg' : ''">
        <icon-solar-ruler-angular-broken style="font-size: 1.5rem; color: white" @click="toggleRuler" />
      </slidebar-icon>
      <slidebar-icon>
        <icon-tabler-exposure-plus-1 style="font-size: 1.5rem; color: white" @click="rulerPlus1" />
      </slidebar-icon>
      <slidebar-icon>
        <icon-tabler-exposure-minus-1 style="font-size: 1.5rem; color: white" @click="rulerMinus1" />
      </slidebar-icon>
    </div>
    <div
      class="h-full w-72 flex bg-gray-700 text-white"
      :key="(state.sidebar.isSubSidebar, state.sidebar.category)"
      v-if="state.sidebar.isSubSidebar">
      <div
        class="h-full w-full flex flex-col overflow-y-scroll scrollbar-gray-100-2"
        :key="(state.sidebar.isSubSidebar, state.sidebar.category)"
        v-if="state.sidebar.category === GalleryImageSideBarEnum.Rotation">
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
