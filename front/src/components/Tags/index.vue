<template>
  <div class="3xl:text-xl">
    <div v-for="(vals, key) in tags" :key="key">
      <tag :fieldKey="key" :fieldValues="vals" :searchable="searchable" :searchBaseUrl="searchBaseUrl" />
    </div>
  </div>
</template>

<script lang="ts">
import { PropType } from "vue";

import Tag from "./Tag.vue";
import { Tags } from "@/interface/gallery";

export default {
  components: { Tag },
  props: {
    tags: {
      type: Object as PropType<Tags>,
      default: {},
    },
    searchable: {
      type: Object as PropType<boolean>,
      default: true,
    },
    searchBaseUrl: {
      type: Object as PropType<string>,
      default: undefined,
    },
  },
  setup(props) {
    return { ...props };
  },
};
</script>
