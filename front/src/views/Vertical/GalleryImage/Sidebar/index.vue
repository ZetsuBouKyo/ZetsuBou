<script setup lang="ts">
import { PropType, ref } from "vue";

import { GalleryImageState } from "../state.inferface";

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

function openRotation() {
  state.modal.rotation.open();
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
</script>

<template>
  <div class="h-app bg-gray-900 flex flex-col items-center">
    <slidebar-icon class="mt-4">
      <icon-entypo-save style="font-size: 1.5rem; color: white" />
    </slidebar-icon>
    <slidebar-icon :class="!state.layers.isEdit ? 'bg-indigo-500 rounded-lg' : ''">
      <icon-clarity-cursor-arrow-solid style="font-size: 1.5rem; color: white" @click="select" />
    </slidebar-icon>
    <slidebar-icon :class="state.layers.isEdit ? 'bg-indigo-500 rounded-lg' : ''">
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
    <slidebar-icon>
      <icon-mdi-arrow-oscillating style="font-size: 1.5rem; color: white" @click="openRotation" />
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
</template>
