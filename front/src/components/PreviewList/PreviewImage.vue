<script setup lang="ts">
import { PropType, reactive, ref, watch } from "vue";

import { Item } from "./interface";

import StarRating from "@/elements/Rating/StarRating.vue";

const props = defineProps({
  item: {
    type: Object as PropType<Item>,
    required: true,
  },
});

const image = ref(null);
const state = reactive({
  loading: true,
  width: undefined,
  height: undefined,
});

function getIntrinsicSize(event) {
  state.width = event.target.naturalWidth;
  state.height = event.target.naturalHeight;
  state.loading = false;
}

watch(
  () => props.item.imgUrl,
  () => {
    state.loading = true;
  },
);
</script>

<template>
  <div class="block relative overflow-hidden rounded-lg my-4 bg-gray-900 hover:shadow-black hover:mt-2 hover:mb-6">
    <div class="m-4">
      <a class="relative" :href="item.linkUrl">
        <img
          ref="image"
          alt="Not found!"
          loading="lazy"
          class="object-contain object-center w-full md:h-72 h-70v block animate-fade-in"
          :class="state.loading ? 'invisible' : ''"
          :title="state.width ? state.width.toString() + ' x ' + state.height.toString() : ''"
          :src="item.imgUrl"
          @load="getIntrinsicSize" />
        <icon-eos-icons-loading
          class="absolute m-auto top-0 bottom-0 left-0 right-0"
          style="font-size: 2rem; color: white"
          v-if="state.loading" />
      </a>
    </div>
    <div class="m-4 3xl:text-base text-xs" v-if="item.category || item.title">
      <div class="flex flex-row items-center mb-1">
        <h3 class="text-gray-500 tracking-widest" v-if="item.category">
          {{ item.category }}
        </h3>
        <div class="ml-auto hover:opacity-50 rounded-lg" v-if="item.srcUrl">
          <a :href="item.srcUrl" :title="item.srcUrl">
            <icon-ic-round-link style="font-size: 1rem; color: white" />
          </a>
        </div>
      </div>
      <div class="flex flex-row">
        <star-rating class="mb-2" :filled="item.rating" />
        <span class="ml-auto text-gray-500" v-if="item.pages">{{ item.pages }} pages</span>
      </div>
      <h2 class="text-white 3xl:text-lg text-base break-words" v-if="item.title">
        {{ item.title }}
      </h2>
      <div class="flex mt-2" v-if="item.lastUpdated">
        <h2 class="text-white ml-auto 3xl:text-xs">Last updated on {{ item.lastUpdated }}</h2>
      </div>
    </div>
  </div>
</template>
