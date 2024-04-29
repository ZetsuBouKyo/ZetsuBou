<template>
    <ripple-button
        class="views-setting-action-ripple-button"
        :class="
            route.path === path
                ? 'views-setting-action-ripple-button-active'
                : 'views-setting-action-ripple-button-inactive'
        "
    >
        <router-link class="views-setting-action" :to="path">
            <slot></slot>
            <span class="views-setting-action-title">{{ title }}</span>
        </router-link>
    </ripple-button>
</template>

<script lang="ts">
import { PropType } from "vue";
import { useRoute } from "vue-router";

import RippleButton from "@/elements/Button/RippleButton.vue";

export default {
    components: { RippleButton },
    props: {
        path: {
            type: Object as PropType<string>,
            default: undefined,
        },
        title: {
            type: Object as PropType<string>,
            default: undefined,
        },
    },
    setup(props) {
        const route = useRoute();
        return { ...props, route };
    },
};
</script>
