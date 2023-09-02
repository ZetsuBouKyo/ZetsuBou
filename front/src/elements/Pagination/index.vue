<script setup lang="ts">
import { onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { Pagination } from "./pagination.interface";

import { detectRouteChange } from "@/utils/route";

const route = useRoute();
const router = useRouter();

onMounted(async () => {
  await router.isReady();
});

interface Props {
  pagination: Pagination;
}
const props = withDefaults(defineProps<Props>(), { pagination: undefined, watchSources: undefined, load: undefined });

function toTop() {
  window.scrollTo(0, 0);
}

watch(
  () => {
    if (props.pagination.watchSources) {
      return [props.pagination.watchSources(), detectRouteChange(route)];
    }
    return [detectRouteChange(route)];
  },
  () => {
    if (props.pagination.load === undefined) {
      return;
    }
    props.pagination.load();
  },
);
</script>

<template>
  <div class="flex text-gray-400" :key="pagination.current">
    <div
      v-if="pagination.pages[0].n > 1 && pagination.pages.length >= pagination.perRound"
      class="h-12 w-12 mr-1 flex justify-center items-center cursor-pointer hover:opacity-50">
      <router-link :to="pagination.toFirstPage" @click="toTop">
        <icon-mdi-chevron-double-left style="font-size: 1.5rem" />
      </router-link>
    </div>
    <div
      v-if="pagination.current > 1 && pagination.pages.length >= pagination.perRound"
      class="h-12 w-12 mr-1 flex justify-center items-center cursor-pointer hover:opacity-50">
      <router-link :to="pagination.toPreviousPage" @click="toTop">
        <icon-mdi-chevron-left style="font-size: 1.5rem" />
      </router-link>
    </div>
    <div class="flex h-12 font-medium">
      <div
        v-if="pagination.pages[0].n > 1"
        class="w-12 md:flex justify-center items-center hidden cursor-default leading-5 transition duration-150">
        ...
      </div>
      <div
        v-for="(p, i) in pagination.pages"
        :key="i"
        class="w-12 md:flex justify-center items-center hidden leading-5 transition duration-150 ease-in">
        <a v-if="p.n === pagination.current" class="text-white cursor-default">{{ p.n }}</a>
        <router-link v-else class="cursor-pointer hover:opacity-50" :to="p.link" @click="toTop">{{ p.n }}</router-link>
      </div>
      <div
        class="w-12 h-12 md:hidden flex justify-center items-center cursor-pointer leading-5 transition duration-150 ease-in rounded-full text-white">
        {{ pagination.current }}
      </div>
      <div
        v-if="pagination.pages[pagination.pages.length - 1].n < pagination.totalPage"
        class="w-12 md:flex justify-center items-center hidden cursor-default leading-5 transition duration-150">
        ...
      </div>
    </div>
    <div
      v-if="pagination.current < pagination.totalPage && pagination.pages.length >= pagination.perRound"
      class="h-12 w-12 mr-1 flex justify-center items-center cursor-pointer hover:opacity-50">
      <router-link :to="pagination.toNextPage" @click="toTop">
        <icon-mdi-chevron-right style="font-size: 1.5rem" />
      </router-link>
    </div>
    <div
      v-if="
        pagination.pages[pagination.pages.length - 1].n < pagination.totalPage &&
        pagination.pages.length >= pagination.perRound
      "
      class="h-12 w-12 mr-1 flex justify-center items-center cursor-pointer hover:opacity-50">
      <router-link :to="pagination.toLastPage" @click="toTop">
        <icon-mdi-chevron-double-right style="font-size: 1.5rem" />
      </router-link>
    </div>
  </div>
</template>
