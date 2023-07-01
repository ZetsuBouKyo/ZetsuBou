<template>
  <svg
    ref="svg"
    :viewBox="svgState.container.viewBox"
    class="h-app w-screen"
    @click="point"
    @wheel="zoom"
    @mousedown="startMoving"
    @mouseup="stopMoving"
    @mousemove="move">
    <image ref="image" class="h-app w-screen" :href="state.imgUrl" :key="state.imgUrl"></image>
    <g v-if="svgState.container.xTopLeft !== undefined && svgState.container.yTopLeft !== undefined">
      <circle :cx="svgState.container.xTopLeft" :cy="svgState.container.yTopLeft" r="2" />
    </g>
    <slot></slot>
  </svg>
</template>

<script lang="ts">
import { ref, reactive, onBeforeMount, nextTick, watch, PropType } from "vue";
import { useRoute } from "vue-router";

import { detectRouteChange } from "@/utils/route";

import SvgLayers from "./SvgLayers.vue";
import { SVG } from "./svg.d";

export default {
  components: { SvgLayers },
  props: {
    svg: {
      type: Object as PropType<SVG>,
      default: undefined,
    },
  },
  setup(props) {
    const svgState = props.svg;

    const route = useRoute();

    const state = reactive({
      gallery: route.params.gallery,
      imgName: route.params.img,
      imgUrl: undefined,
    });

    let svg = ref(null);
    let image = ref(null);

    function getImgUrl() {
      return `/api/v1/gallery/${state.gallery}/i/${state.imgName}`;
    }

    function load() {
      if (route.params.gallery === undefined || route.params.img === undefined) {
        return;
      }
      svgState.container.viewBox = undefined;

      state.gallery = route.params.gallery;
      state.imgName = route.params.img;
      state.imgUrl = getImgUrl();
      setImageSlope();
      document.addEventListener.call(window, "resize", () => {
        setImageSlope();
      });
      document.addEventListener.call(window, "keyup", (event) => {
        if (event.keyCode === 13) {
          finishSelection();
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

    function setImageSlope() {
      let tmpImg = new Image();
      tmpImg.src = state.imgUrl;
      tmpImg.onload = () => {
        svgState.container.imgWidth = tmpImg.width;
        svgState.container.imgHeight = tmpImg.height;
        svgState.container.imgSlope = svgState.container.imgHeight / svgState.container.imgWidth;
        setOrigin();
      };
    }

    function setOrigin() {
      if (svg.value === null) {
        return;
      }
      const svgWidth = svg.value.getBoundingClientRect().width;
      const svgHeight = svg.value.getBoundingClientRect().height;
      const svgSlope = svgHeight / svgWidth;

      if (svgSlope > svgState.container.imgSlope) {
        svgState.container.xTopLeft = 0;
        svgState.container.yTopLeft = (svgHeight - svgWidth * svgState.container.imgSlope) / 2;
        svgState.container.xBottomRight = svgWidth;
        svgState.container.yBottomRight = svgState.container.yTopLeft + svgWidth * svgState.container.imgSlope;
      } else {
        svgState.container.xTopLeft = (svgWidth - svgHeight / svgState.container.imgSlope) / 2;
        svgState.container.yTopLeft = 0;
        svgState.container.xBottomRight = svgState.container.xTopLeft + svgHeight / svgState.container.imgSlope;
        svgState.container.yBottomRight = svgHeight;
      }
    }

    onBeforeMount(() => {});

    watch(
      () => [svgState.container.imgSlope, svgState.sidebar.isSidebar],
      () => {
        setImageSlope();
      },
    );

    function startMoving() {
      if (svgState.layers.isEdit) {
        return;
      }
      svgState.container.draggable = true;
    }

    function stopMoving() {
      if (svgState.layers.isEdit) {
        return;
      }
      svgState.container.draggable = false;
    }

    function move(event) {
      if (svgState.container.draggable) {
        let clientInSvg = svg.value.createSVGPoint();
        clientInSvg.x = event.clientX;
        clientInSvg.y = event.clientY;
        let ctm = svg.value.getScreenCTM();
        let initial = clientInSvg.matrixTransform(ctm.inverse());
        let clientMovingInSvg = svg.value.createSVGPoint();
        clientMovingInSvg.x = event.clientX + event.movementX;
        clientMovingInSvg.y = event.clientY + event.movementY;
        let final = clientMovingInSvg.matrixTransform(ctm.inverse());
        let dx = initial.x - final.x;
        let dy = initial.y - final.y;

        let viewBoxValues;
        if (svgState.container.viewBox === undefined) {
          viewBoxValues = [0, 0, svg.value.width.baseVal.value, svg.value.height.baseVal.value];
        } else {
          viewBoxValues = svgState.container.viewBox.split(" ").map((n) => parseFloat(n));
        }
        let x0 = (viewBoxValues[0] + dx).toString();
        let y0 = (viewBoxValues[1] + dy).toString();
        let w = viewBoxValues[2].toString();
        let h = viewBoxValues[3].toString();
        svgState.container.viewBox = `${x0} ${y0} ${w} ${h}`;
      }
    }

    function getZoomRatio(event: any) {
      let r: number;
      if (event.deltaY > 0) {
        r = 0.9;
      } else if (event.deltaY < 0) {
        r = 1.1;
      } else {
        r = 1;
      }
      return r;
    }

    function zoom(event: any) {
      const r: number = getZoomRatio(event);
      const cX = event.clientX;
      const cY = event.clientY;

      let viewBoxValues: Array<number>;
      if (svgState.container.viewBox === undefined) {
        viewBoxValues = [0, 0, svg.value.width.baseVal.value, svg.value.height.baseVal.value];
      } else {
        viewBoxValues = svgState.container.viewBox.split(" ").map((n) => parseFloat(n));
      }

      let [x0, y0, w, h]: Array<number> = viewBoxValues;
      w = w / r;
      h = h / r;
      let clientInSvg = svg.value.createSVGPoint();
      clientInSvg.x = cX;
      clientInSvg.y = cY;
      let ctmInitial = svg.value.getScreenCTM();
      let svgCoorInitial = clientInSvg.matrixTransform(ctmInitial.inverse());
      svgState.container.viewBox = `${x0} ${y0} ${w} ${h}`;

      nextTick(() => {
        let ctmFinal = svg.value.getScreenCTM();
        let svgCoorFinal = clientInSvg.matrixTransform(ctmFinal.inverse());
        let dx = svgCoorInitial.x - svgCoorFinal.x ? svgCoorInitial.x - svgCoorFinal.x : 0;
        let dy = svgCoorInitial.y - svgCoorFinal.y ? svgCoorInitial.y - svgCoorFinal.y : 0;
        let sViewBoxValue2 = svgState.container.viewBox.split(" ").map((n) => parseFloat(n));
        svgState.container.viewBox =
          (sViewBoxValue2[0] + dx).toString() +
          " " +
          (sViewBoxValue2[1] + dy).toString() +
          " " +
          sViewBoxValue2[2].toString() +
          " " +
          sViewBoxValue2[3].toString();
      });
    }

    function point(event: any) {
      if (
        !svgState.layers.isEdit ||
        !svgState.sidebar.isSidebar ||
        svgState.layers.current.layer === undefined ||
        svgState.layers.current.selection === undefined
      ) {
        return;
      }

      let x = event.clientX;
      let y = event.clientY;
      let pts = svg.value.createSVGPoint();
      pts.x = x;
      pts.y = y;

      let newPts = pts.matrixTransform(svg.value.getScreenCTM().inverse());
      // console.log(newPts);
      let newX: number;
      if (newPts.x < svgState.container.xTopLeft) {
        newX = svgState.container.xTopLeft;
      } else if (newPts.x > svgState.container.xBottomRight) {
        newX = svgState.container.xBottomRight;
      } else {
        newX = newPts.x;
      }
      let newY: number;
      if (newPts.y < svgState.container.yTopLeft) {
        newY = svgState.container.yTopLeft;
      } else if (newPts.y > svgState.container.yBottomRight) {
        newY = svgState.container.yBottomRight;
      } else {
        newY = newPts.y;
      }

      const layerIndex = svgState.layers.current.layer as number;
      const selectionIndex = svgState.layers.current.selection as number;

      svgState.layers.layers[layerIndex].selections[selectionIndex].points.push({
        x: newX,
        y: newY,
      });
    }

    function finishSelection() {
      const layerIndex = svgState.layers.current.layer as number;
      const selectionIndex = svgState.layers.current.selection as number;

      svgState.layers.layers[layerIndex].selections[selectionIndex].isCompleted = true;
      svgState.layers.current.layer = undefined;
      svgState.layers.current.selection = undefined;
    }

    return {
      getImgUrl,
      image,
      move,
      point,
      startMoving,
      state,
      stopMoving,
      svg,
      svgState,
      zoom,
    };
  },
};
</script>
