<template>
  <div class="flex flex-row">
    <sidebar class="animate-slide-in fixed top-20 left-0" :layerState="layerState" v-if="tagger.isTagger" />
    <svg-container ref="svg" :tagger="tagger" :layerState="layerState">
      <svg-layers v-if="tagger.isTagger" :state="layerState" />
    </svg-container>
  </div>
</template>

<script lang="ts">
import { useRoute } from "vue-router";
import { ref, reactive, onMounted, onBeforeMount, nextTick, watch } from "vue";

import SvgContainer from "./SvgContainer.vue";
import SvgLayers from "./SvgLayers.vue";
import Sidebar from "./Sidebar/index.vue";
import { LayerState } from "./interface";

export default {
  components: { SvgLayers, SvgContainer, Sidebar },
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

    let svg = ref(null);

    const layerState = reactive<LayerState>({
      current: {
        layer: 0,
        selection: 0,
      },
      isEdit: false,
      layers: [],
    });

    function getColor() {
      const r: number = Math.floor(Math.random() * 256);
      const g: number = Math.floor(Math.random() * 256);
      const b: number = Math.floor(Math.random() * 256);
      const rgb: Array<number> = [r, g, b];
      return `rgb(${rgb.join(",")})`;
    }

    layerState.layers.push({
      name: "Default",
      show: true,
      selections: [
        {
          color: getColor(),
          isCompleted: false,
          points: [],
        },
      ],
    });

    return {
      tagger,
      svg,
      layerState,
    };
  },
};
</script>
