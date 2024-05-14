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
      <icon-mdi-arrow-oscillating style="font-size: 1.5rem; color: white" @click="openRotation" />
    </slidebar-icon>
    <slidebar-icon :class="state.sidebar.isRuler ? 'bg-gray-500 rounded-lg' : ''">
      <icon-solar-ruler-angular-broken style="font-size: 1.5rem; color: white" @click="toggleRuler" />
    </slidebar-icon>
  </div>
</template>
