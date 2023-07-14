<script setup lang="ts">
import { PropType } from "vue";

import { SVG } from "../svg.interface";

import SlidebarIcon from "./SlidebarIcon.vue";

const props = defineProps({
  svg: {
    type: Object as PropType<SVG>,
    required: true,
  },
});

const layerState = props.svg.layers;

function select() {
  layerState.isEdit = false;
}

function edit() {
  layerState.isEdit = true;
}
</script>

<template>
  <div class="h-app bg-gray-900 flex flex-col items-center">
    <slidebar-icon class="mt-4">
      <icon-entypo-save style="font-size: 1.5rem; color: white" />
    </slidebar-icon>
    <slidebar-icon :class="!layerState.isEdit ? 'bg-indigo-500 rounded-lg' : ''">
      <icon-clarity-cursor-arrow-solid style="font-size: 1.5rem; color: white" @click="select" />
    </slidebar-icon>
    <slidebar-icon :class="layerState.isEdit ? 'bg-indigo-500 rounded-lg' : ''">
      <icon-mdi-vector-polygon style="font-size: 1.5rem; color: white" @click="edit" />
    </slidebar-icon>
    <slidebar-icon>
      <icon-ion-ios-pricetags style="font-size: 1.5rem; color: white" />
    </slidebar-icon>
    <slidebar-icon>
      <icon-whh-layerorderup style="font-size: 1.5rem; color: white" />
    </slidebar-icon>
  </div>
</template>
