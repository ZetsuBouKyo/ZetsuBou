<template>
  <datalist>
    <option class="modal-row" :key="key" :value="val" v-for="(val, key) in state.options" />
  </datalist>
</template>

<script lang="ts">
import { reactive, watch, PropType } from "vue";

import { getTagTokenStartWith } from "@/api/v1/tag/token";

import { SearchState } from "@/interface/search";

export default {
  props: {
    searchState: {
      type: Object as PropType<SearchState>,
      default: undefined,
    },
  },
  setup(props) {
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
          state.options = [...new Set(state.options)];
        });
      },
    );
    return { state };
  },
};
</script>
