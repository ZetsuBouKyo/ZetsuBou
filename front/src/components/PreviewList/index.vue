<script setup lang="ts">
import Pagination from "./Pagination.vue";
import PreviewImage from "./PreviewImage.vue";

import { previewsState } from "./previews.state";
</script>

<template>
  <section class="body-font min-h-screen" v-if="previewsState.items && previewsState.items.length > 0">
    <pagination
      class="sticky top-20 z-40 bg-gray-800"
      :pagination="previewsState.pagination"
      :key="JSON.stringify(previewsState.pagination)" />
    <div class="px-5 py-5 mx-auto">
      <div class="flex flex-wrap -m-4">
        <div class="3xl:w-1/10 xl:w-1/6 lg:w-1/4 md:w-1/2 p-4 w-full" v-for="(item, i) in previewsState.items" :key="i">
          <preview-image :item="item" />
        </div>
      </div>
    </div>
  </section>
  <section
    class="body-font min-h-screen"
    v-else-if="previewsState.items === undefined && previewsState.pagination === undefined">
    <header>
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 h-app">
        <icon-eos-icons-loading class="m-auto h-full animate-spin" style="font-size: 2rem; color: white" />
      </div>
    </header>
  </section>
  <section v-else>
    <header>
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 h-app">
        <h1 class="text-3xl font-bold leading-tight">No results</h1>
      </div>
    </header>
  </section>
</template>
