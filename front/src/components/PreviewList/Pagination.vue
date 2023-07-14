<script setup lang="ts">
import { PropType } from "vue";

import { Pagination } from "@/elements/Pagination/pagination.interface";

import PaginationBase from "@/elements/Pagination/index.vue";

defineProps({
  pagination: {
    type: Object as PropType<Pagination>,
    required: true,
  },
});

// onBeforeMount(() => {
//   document.addEventListener.call(window, "keyup", (event) => {
//     if (event.keyCode === 34 && pagination.current < pagination.totalPage) {
//       router.push(pagination.toNextPage);
//     } else if (event.keyCode === 33 && pagination.current > 1) {
//       router.push(pagination.toPreviousPage);
//     }
//   });
// });
</script>

<template>
  <div
    v-if="pagination && pagination.pages.length > 0"
    class="flex flex-col items-center bg-opacity-75 z-40 3xl:text-xl">
    <span class="mt-5 text-gray-200" v-if="pagination.totalItems">Total: {{ pagination.totalItems }}</span>
    <pagination-base :pagination="pagination" />
  </div>
</template>
