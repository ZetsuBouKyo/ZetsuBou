<script setup lang="ts">
import RippleAnchor from "@/elements/Anchor/RippleAnchor.vue";

interface Props {
  fieldKey: string | number;
  fieldValues: Array<string>;
  searchable?: boolean;
  searchBaseUrl?: string;
}
const props = withDefaults(defineProps<Props>(), {
  searchable: true,
  searchBaseUrl: undefined,
});

function search(field: string | number, value: string) {
  return `${props.searchBaseUrl}?tag_field_1=${field}&tag_value_1=${value}`;
}
</script>

<template>
  <div class="flex flex-row my-2">
    <span class="w-min my-1 3xl:py-2 py-1 text-gray-100">{{ fieldKey }}:&nbsp;&nbsp;</span>
    <div class="flex flex-wrap w-full text-gray-900">
      <ripple-anchor
        class="truncate transition-colors duration-200 ease-in m-1 3xl:px-4 3xl:py-2 px-3 py-1 bg-gray-200 rounded-full max-w-48 lg:max-w-96"
        :class="
          searchable ? 'cursor-pointer hover:bg-indigo-500 hover:text-gray-100 hover:border-white' : 'cursor-default'
        "
        v-for="(val, i) in fieldValues"
        :key="i"
        :href="searchable ? search(fieldKey, val) : undefined">
        {{ val }}
      </ripple-anchor>
    </div>
  </div>
</template>
