<template>
    <div class="views-setting-action-ripple-button setting-action-ripple-button-inactive">
        <div class="views-setting-action">
            <span class="views-setting-sub-action">&emsp;&emsp;&emsp;{{ title }}</span>
        </div>
    </div>
</template>

<script lang="ts">
import { PropType } from "vue";

export default {
    props: {
        title: {
            type: Object as PropType<string>,
            default: undefined,
        },
    },
    setup(props) {
        return { ...props };
    },
};
</script>
