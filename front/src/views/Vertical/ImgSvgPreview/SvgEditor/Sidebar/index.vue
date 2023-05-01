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

<script lang="ts">
import { useRoute } from "vue-router";
import { ref, reactive, onMounted, onBeforeMount, nextTick, watch, PropType } from "vue";

import { LayerState } from "../interface";
import SlidebarIcon from "./SlidebarIcon.vue";

export default {
  components: { SlidebarIcon },
  props: {
    layerState: {
      type: Object as PropType<LayerState>,
      default: undefined,
    },
  },
  setup(props) {
    const route = useRoute();
    const gallery = route.params.gallery;
    const layerState = props.layerState;

    function select() {
      layerState.isEdit = false;
    }

    function edit() {
      layerState.isEdit = true;
    }

    function back() {
      const url = "/g/" + gallery;
      window.open(url, "_self");
    }

    return {
      layerState,
      select,
      edit,
      back,
    };
  },
};
</script>
