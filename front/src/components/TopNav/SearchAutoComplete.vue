<script setup lang="ts">
import { PropType, reactive, watch } from "vue";

import { SearchState } from "@/interface/search";

import { getTagTokenStartWith } from "@/api/v1/tag/token";

const props = defineProps({
  searchState: {
    type: Object as PropType<SearchState>,
    required: true,
  },
});

const searchState = props.searchState;
const state = reactive({
  options: [],
});

watch(
  () => searchState.query.keywords,
  () => {
    state.options = [];
    if (!searchState.query.keywords) {
      return;
    }

    getTagTokenStartWith({ s: searchState.query.keywords }).then((response: any) => {
      const data = response.data;
      for (const token of data) {
        state.options.push(token.name);
      }
      state.options = Array.from(new Set(state.options));
    });
  },
);
</script>

<template>
  <datalist>
    <option class="modal-row" :key="key" :value="val" v-for="(val, key) in state.options" />
  </datalist>
</template>
