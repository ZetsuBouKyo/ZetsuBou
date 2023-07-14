<script setup lang="ts">
import { Tags } from "@/interface/tag";

import Tag from "./Tag.vue";

interface Props {
  tags?: Tags;
  searchable?: boolean;
  searchBaseUrl?: string;
}
withDefaults(defineProps<Props>(), {
  tags: () => <Tags>{},
  searchable: true,
  searchBaseUrl: undefined,
});
</script>

<template>
  <div class="3xl:text-xl">
    <div v-for="(vals, key) in tags" :key="key">
      <tag :field-key="key" :field-values="vals" :searchable="searchable" :search-baseUrl="searchBaseUrl" />
    </div>
  </div>
</template>
