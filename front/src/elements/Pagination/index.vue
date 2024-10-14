<script setup lang="ts">
import { PropType, reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";

import { Pagination } from "./pagination.interface";

import { getPageUrl } from "@/elements/Pagination/pagination";

import { isPositiveInteger } from "@/utils/number";

const leftInput = ref();
const rightInput = ref();
const router = useRouter();

const props = defineProps({
    pagination: {
        type: Object as PropType<Pagination>,
        required: true,
    },
});

const pagination = props.pagination;

const privateState = reactive({
    page: undefined,
    editLeft: false,
    editRight: false,
});

function inputFocusOut() {
    privateState.editLeft = false;
    privateState.editRight = false;
}

function togglePageLeftInput() {
    privateState.editLeft = true;
    privateState.editRight = false;
}

watch(
    () => leftInput.value,
    () => {
        if (!leftInput.value) {
            return;
        }
        leftInput.value.focus();
    },
);

function togglePageRightInput() {
    privateState.editLeft = false;
    privateState.editRight = true;
}

watch(
    () => rightInput.value,
    () => {
        if (!rightInput.value) {
            return;
        }
        rightInput.value.focus();
    },
);

function jump() {
    const page = Number(privateState.page);
    if (!isPositiveInteger(page) || page > pagination.totalPage || page === 0) {
        return;
    }
    const url = getPageUrl(page, pagination.path, pagination.query);
    router.push(url);
}

function toTop() {
    window.scrollTo(0, 0);
}
</script>

<template>
    <div class="flex text-gray-400" :key="pagination.current">
        <div
            v-if="pagination.pages[0].n > 1 && pagination.pages.length >= pagination.perRound"
            class="h-12 w-12 mr-1 flex justify-center items-center cursor-pointer hover:opacity-50"
        >
            <router-link :to="pagination.toFirstPage" @click="toTop">
                <icon-mdi-chevron-double-left style="font-size: 1.5rem" />
            </router-link>
        </div>
        <div
            v-if="pagination.current > 1 && pagination.pages.length >= pagination.perRound"
            class="h-12 w-12 mr-1 flex justify-center items-center cursor-pointer hover:opacity-50"
        >
            <router-link :to="pagination.toPreviousPage" @click="toTop">
                <icon-mdi-chevron-left style="font-size: 1.5rem" />
            </router-link>
        </div>
        <div class="flex h-12 font-medium">
            <div
                v-if="pagination.pages[0].n > 1"
                class="w-12 md:flex justify-center items-center hidden cursor-default leading-5 transition duration-150"
            >
                <div @click="togglePageLeftInput" v-if="!privateState.editLeft">...</div>
                <input
                    ref="leftInput"
                    class="w-14 px-2 rounded-md border-gray-700 bg-gray-700 text-white placeholder-gray-400 focus:outline-none text-center"
                    :placeholder="pagination.totalPage.toString()"
                    v-model="privateState.page"
                    @focusout="inputFocusOut"
                    @keyup.enter="jump"
                    v-else
                />
            </div>
            <div
                v-for="(p, i) in pagination.pages"
                :key="i"
                class="mx-4 md:flex justify-center items-center hidden leading-5 transition duration-150 ease-in"
            >
                <a v-if="p.n === pagination.current" class="text-white cursor-default">{{ p.n }}</a>
                <router-link v-else class="cursor-pointer hover:opacity-50" :to="p.link" @click="toTop">{{
                    p.n
                }}</router-link>
            </div>
            <div
                class="w-12 h-12 md:hidden flex justify-center items-center cursor-pointer leading-5 transition duration-150 ease-in rounded-full text-white"
            >
                {{ pagination.current }}
            </div>
            <div
                v-if="pagination.pages[pagination.pages.length - 1].n < pagination.totalPage"
                class="w-12 md:flex justify-center items-center hidden cursor-default leading-5 transition duration-150"
            >
                <div @click="togglePageRightInput" v-if="!privateState.editRight">...</div>
                <input
                    ref="rightInput"
                    class="w-14 px-2 rounded-md border-gray-700 bg-gray-700 text-white placeholder-gray-400 focus:outline-none text-center"
                    :placeholder="pagination.totalPage.toString()"
                    v-model="privateState.page"
                    @focusout="inputFocusOut"
                    @keyup.enter="jump"
                    v-else
                />
            </div>
        </div>
        <div
            v-if="pagination.current < pagination.totalPage && pagination.pages.length >= pagination.perRound"
            class="h-12 w-12 mr-1 flex justify-center items-center cursor-pointer hover:opacity-50"
        >
            <router-link :to="pagination.toNextPage" @click="toTop">
                <icon-mdi-chevron-right style="font-size: 1.5rem" />
            </router-link>
        </div>
        <div
            v-if="
                pagination.pages[pagination.pages.length - 1].n < pagination.totalPage &&
                pagination.pages.length >= pagination.perRound
            "
            class="h-12 w-12 mr-1 flex justify-center items-center cursor-pointer hover:opacity-50"
        >
            <router-link :to="pagination.toLastPage" @click="toTop">
                <icon-mdi-chevron-double-right style="font-size: 1.5rem" />
            </router-link>
        </div>
    </div>
</template>
