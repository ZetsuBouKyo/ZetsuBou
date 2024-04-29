<script setup lang="ts">
import { useRoute } from "vue-router";

import { Tabs } from "./interface";

interface Props {
    tabs: Tabs;
}
const props = withDefaults(defineProps<Props>(), {
    tabs: undefined,
});

const route = useRoute();
const tabs = props.tabs;

for (let i = 0; i < tabs.length; i++) {
    if (tabs[i].link === route.path) {
        tabs[i].active = true;
    }
}
</script>

<template>
    <div class="flex mx-auto overflow-x-hidden">
        <a
            v-for="(tab, i) in tabs"
            :key="i"
            class="flex-grow pr-8 py-2 text-lg border-b-2"
            :class="
                tab.active
                    ? 'text-indigo-400 border-indigo-500 cursor-default'
                    : 'text-gray-100 border-gray-200 cursor-pointer hover:opacity-50'
            "
            :href="tab.active ? undefined : tab.link"
            >{{ tab.title }}</a
        >
    </div>
</template>
