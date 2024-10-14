<script setup lang="ts">
import { PropType } from "vue";

import { SVG } from "./svg.interface";

defineProps({
    svg: {
        type: Object as PropType<SVG>,
        required: true,
    },
});
</script>

<template>
    <g v-for="(layer, i) in svg.layers.layers" :key="i">
        <g v-if="layer.show">
            <g v-for="(selection, i) in layer.selections" :key="i">
                <g>
                    <circle
                        v-for="(point, i) in selection.points"
                        :key="i"
                        :fill="selection.color"
                        :cx="point.x"
                        :cy="point.y"
                        stroke="rgb(255,255,255)"
                        r="4"
                    />
                </g>
                <g>
                    <g v-for="(point, i) in selection.points" :key="i">
                        <line
                            v-if="i > 0"
                            :x1="selection.points[i - 1].x"
                            :y1="selection.points[i - 1].y"
                            :x2="selection.points[i].x"
                            :y2="selection.points[i].y"
                            :stroke="selection.color"
                        />
                    </g>
                    <g v-if="selection.isCompleted">
                        <line
                            :x1="selection.points[selection.points.length - 1].x"
                            :y1="selection.points[selection.points.length - 1].y"
                            :x2="selection.points[0].x"
                            :y2="selection.points[0].y"
                            :stroke="selection.color"
                        />
                    </g>
                </g>
            </g>
        </g>
    </g>
</template>
