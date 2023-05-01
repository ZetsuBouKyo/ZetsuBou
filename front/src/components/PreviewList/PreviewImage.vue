<script lang="ts">
import { ref, reactive, PropType } from "vue";

import { Item } from "./interface";
import StarRating from "@/elements/Rating/StarRating.vue";

export default {
  components: { StarRating },
  props: {
    item: {
      type: Object as PropType<Item>,
      default: undefined,
    },
  },
  setup(props) {
    let image = ref(null);
    const state = reactive({
      width: undefined,
      height: undefined,
    });

    function getIntrinsicSize(event) {
      state.width = event.target.naturalWidth;
      state.height = event.target.naturalHeight;
    }

    return { ...props, state, image, getIntrinsicSize };
  },
};
</script>

<template>
  <div>
    <div class="block relative overflow-hidden rounded-lg bg-gray-900">
      <div class="m-4 hover:opacity-50">
        <a :href="item.linkUrl">
          <img
            ref="image"
            alt="Not found!"
            loading="lazy"
            class="object-contain object-center w-full md:h-72 h-70v block animate-fade-in"
            :title="state.width ? state.width.toString() + ' x ' + state.height.toString() : ''"
            :src="item.imgUrl"
            @load="getIntrinsicSize"
          />
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
        <star-rating class="mb-2" :filled="item.rating" />
        <h2 class="text-white 3xl:text-lg text-base break-words" v-if="item.title">
          {{ item.title }}
        </h2>
        <div class="flex mt-2" v-if="item.timestamp">
          <h2 class="text-white text-gray-500 ml-auto 3xl:text-xs">Last updated on {{ item.timestamp }}</h2>
        </div>
      </div>
    </div>
  </div>
</template>
