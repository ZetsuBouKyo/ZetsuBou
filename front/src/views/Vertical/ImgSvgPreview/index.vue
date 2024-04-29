<script setup lang="ts">
import { reactive } from "vue";
import { useRoute } from "vue-router";

import { SVG } from "./SvgEditor/svg.interface";

import PlayPanel from "./PlayPanel.vue";
import SvgEditor from "./SvgEditor/index.vue";

const route = useRoute();

const svgState = reactive<SVG>({
    container: {
        draggable: false,
        viewBox: undefined,
        imgWidth: undefined,
        imgHeight: undefined,
        imgSlope: undefined,
        xTopLeft: undefined,
        yTopLeft: undefined,
        xBottomRight: undefined,
        yBottomRight: undefined,
    },
    bookmark: {
        isBookmark: false,
    },
    sidebar: {
        isSidebar: false,
        activateSidebar: () => {
            svgState.sidebar.isSidebar = true;
        },
        closeSidebar: () => {
            svgState.sidebar.isSidebar = false;
        },
        toggleSidebar: () => {
            svgState.sidebar.isSidebar = !svgState.sidebar.isSidebar;
        },
    },
    panel: {
        imgs: [],
        galleryID: route.params.gallery as string,
        imgName: route.params.img as string,
        timeInterval: route.query.interval ? parseInt(route.query.interval as string) : 5,
        current: undefined,
        isPlay: route.query.play as any,
        play: undefined,
    },
    layers: {
        current: {
            layer: 0,
            selection: 0,
        },
        isEdit: false,
        layers: [],
    },
    ruler: {
        show: false,
        isEdit: false,
        interval: 5,
        color: "rgb(0,0,0)",
    },
});
</script>

<template>
    <svg-editor :svg="svgState" />
    <play-panel :svg="svgState" />
</template>
