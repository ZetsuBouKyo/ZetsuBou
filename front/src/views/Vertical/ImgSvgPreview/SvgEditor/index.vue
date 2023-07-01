<template>
  <div class="flex flex-row">
    <sidebar class="animate-slide-in fixed top-20 left-0" :svg="svgState" v-if="svgState.sidebar.isSidebar" />
    <svg-container ref="svg" :svg="svgState">
      <svg-layers v-if="svgState.sidebar.isSidebar" :svg="svgState" />
    </svg-container>
  </div>
</template>

<script lang="ts">
import { PropType, ref } from "vue";

import SvgContainer from "./SvgContainer.vue";
import SvgLayers from "./SvgLayers.vue";
import Sidebar from "./Sidebar/index.vue";
import { SVG } from "./svg.d";

export default {
  components: { SvgLayers, SvgContainer, Sidebar },
  props: {
    svg: {
      type: Object as PropType<SVG>,
      default: undefined,
    },
  },
  setup(props) {
    const svgState = props.svg;
    let svg = ref(null);

    function getColor() {
      const r: number = Math.floor(Math.random() * 256);
      const g: number = Math.floor(Math.random() * 256);
      const b: number = Math.floor(Math.random() * 256);
      const rgb: Array<number> = [r, g, b];
      return `rgb(${rgb.join(",")})`;
    }

    svgState.layers.layers.push({
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
      svg,
      svgState,
    };
  },
};
</script>
