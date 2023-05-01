<template>
  <svg
    ref="svg"
    :viewBox="svgState.viewBox"
    class="h-app w-screen"
    @click="point"
    @wheel="zoom"
    @mousedown="startMoving"
    @mouseup="stopMoving"
    @mousemove="move"
  >
    <image ref="image" class="h-app w-screen" :href="getImgUrl()"></image>
    <g v-if="svgState.xTopLeft !== undefined && svgState.yTopLeft !== undefined">
      <circle :cx="svgState.xTopLeft" :cy="svgState.yTopLeft" r="2" />
    </g>
    <slot></slot>
  </svg>
</template>

<script lang="ts">
import { useRoute } from "vue-router";
import { ref, reactive, onMounted, onBeforeMount, nextTick, watch, PropType } from "vue";

import SvgLayers from "./SvgLayers.vue";
import { LayerState } from "./interface";

export default {
  components: { SvgLayers },
  props: {
    tagger: {
      type: Object,
      default: undefined,
    },
    layerState: {
      type: Object as PropType<LayerState>,
      default: undefined,
    },
  },
  setup(props) {
    const tagger = props.tagger;
    const layerState = props.layerState;

    const route = useRoute();
    const gallery = route.params.gallery;
    const imgName = route.params.img;

    let svg = ref(null);
    let image = ref(null);

    const svgState = reactive({
      draggable: false,
      viewBox: undefined,
      imgWidth: undefined,
      imgHeight: undefined,
      imgSlope: undefined,
      xTopLeft: undefined,
      yTopLeft: undefined,
      xBottomRight: undefined,
      yBottomRight: undefined,
    });

    function getImgUrl() {
      return `/api/v1/gallery/${gallery}/i/${imgName}`;
    }

    function setImageSlope() {
      let tmpImg = new Image();
      tmpImg.src = getImgUrl();
      tmpImg.onload = () => {
        svgState.imgWidth = tmpImg.width;
        svgState.imgHeight = tmpImg.height;
        svgState.imgSlope = svgState.imgHeight / svgState.imgWidth;
        setOrigin();
      };
    }

    function setOrigin() {
      const svgWidth = svg.value.getBoundingClientRect().width;
      const svgHeight = svg.value.getBoundingClientRect().height;
      const svgSlope = svgHeight / svgWidth;

      if (svgSlope > svgState.imgSlope) {
        svgState.xTopLeft = 0;
        svgState.yTopLeft = (svgHeight - svgWidth * svgState.imgSlope) / 2;
        svgState.xBottomRight = svgWidth;
        svgState.yBottomRight = svgState.yTopLeft + svgWidth * svgState.imgSlope;
      } else {
        svgState.xTopLeft = (svgWidth - svgHeight / svgState.imgSlope) / 2;
        svgState.yTopLeft = 0;
        svgState.xBottomRight = svgState.xTopLeft + svgHeight / svgState.imgSlope;
        svgState.yBottomRight = svgHeight;
      }
    }

    onBeforeMount(() => {
      setImageSlope();
      document.addEventListener.call(window, "resize", () => {
        setImageSlope();
      });
      document.addEventListener.call(window, "keyup", (event) => {
        if (event.keyCode === 13) {
          finishSelection();
        }
      });
    });

    watch(
      () => [svgState.imgSlope, tagger.isTagger],
      () => {
        setImageSlope();
      },
    );

    onMounted(() => {});

    function startMoving() {
      if (layerState.isEdit) {
        return;
      }
      svgState.draggable = true;
    }

    function stopMoving() {
      if (layerState.isEdit) {
        return;
      }
      svgState.draggable = false;
    }

    function move(event) {
      if (svgState.draggable) {
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
        if (svgState.viewBox === undefined) {
          viewBoxValues = [0, 0, svg.value.width.baseVal.value, svg.value.height.baseVal.value];
        } else {
          viewBoxValues = svgState.viewBox.split(" ").map((n) => parseFloat(n));
        }
        let x0 = (viewBoxValues[0] + dx).toString();
        let y0 = (viewBoxValues[1] + dy).toString();
        let w = viewBoxValues[2].toString();
        let h = viewBoxValues[3].toString();
        svgState.viewBox = `${x0} ${y0} ${w} ${h}`;
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
      if (svgState.viewBox === undefined) {
        viewBoxValues = [0, 0, svg.value.width.baseVal.value, svg.value.height.baseVal.value];
      } else {
        viewBoxValues = svgState.viewBox.split(" ").map((n) => parseFloat(n));
      }

      let [x0, y0, w, h]: Array<number> = viewBoxValues;
      w = w / r;
      h = h / r;
      let clientInSvg = svg.value.createSVGPoint();
      clientInSvg.x = cX;
      clientInSvg.y = cY;
      let ctmInitial = svg.value.getScreenCTM();
      let svgCoorInitial = clientInSvg.matrixTransform(ctmInitial.inverse());
      svgState.viewBox = `${x0} ${y0} ${w} ${h}`;

      nextTick(() => {
        let ctmFinal = svg.value.getScreenCTM();
        let svgCoorFinal = clientInSvg.matrixTransform(ctmFinal.inverse());
        let dx = svgCoorInitial.x - svgCoorFinal.x ? svgCoorInitial.x - svgCoorFinal.x : 0;
        let dy = svgCoorInitial.y - svgCoorFinal.y ? svgCoorInitial.y - svgCoorFinal.y : 0;
        let sViewBoxValue2 = svgState.viewBox.split(" ").map((n) => parseFloat(n));
        svgState.viewBox =
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
        !layerState.isEdit ||
        !tagger.isTagger ||
        layerState.current.layer === undefined ||
        layerState.current.selection === undefined
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
      let newX: Number;
      if (newPts.x < svgState.xTopLeft) {
        newX = svgState.xTopLeft;
      } else if (newPts.x > svgState.xBottomRight) {
        newX = svgState.xBottomRight;
      } else {
        newX = newPts.x;
      }
      let newY: Number;
      if (newPts.y < svgState.yTopLeft) {
        newY = svgState.yTopLeft;
      } else if (newPts.y > svgState.yBottomRight) {
        newY = svgState.yBottomRight;
      } else {
        newY = newPts.y;
      }

      const layerIndex = layerState.current.layer;
      const selectionIndex = layerState.current.selection;

      layerState.layers[layerIndex].selections[selectionIndex].points.push({
        x: newX,
        y: newY,
      });
    }

    function finishSelection() {
      const layerIndex = layerState.current.layer;
      const selectionIndex = layerState.current.selection;

      layerState.layers[layerIndex].selections[selectionIndex].isCompleted = true;
      layerState.current.layer = undefined;
      layerState.current.selection = undefined;
    }

    return {
      tagger,
      image,
      svg,
      svgState,
      layerState,
      getImgUrl,
      move,
      startMoving,
      stopMoving,
      zoom,
      point,
    };
  },
};
</script>
