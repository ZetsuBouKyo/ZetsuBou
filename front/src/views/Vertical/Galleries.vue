<template>
  <div>
    <preview-list :previews="previews" />
  </div>
</template>

<script lang="ts">
import { reactive, watch } from "vue";
import { useRoute } from "vue-router";

import { getDatetime } from "@/utils/datetime";

import { getRandom, getAdvancedSearch, getSearch, SearchQuery } from "@/api/v1/gallery/query";

import { userState } from "@/state/user";

import { getPagination } from "@/elements/Pagination/pagination";
import { Item, Items, Previews } from "@/components/PreviewList/interface";

import PreviewList from "@/components/PreviewList/index.vue";

function getItems(hits: any) {
  let items: Items = [];
  for (let i = 0; i < hits.length; i++) {
    let id = hits[i]._id;
    let item: Item = {
      category: hits[i]._source.attributes.category,
      rating: hits[i]._source.attributes.rating,
      title: hits[i]._source.attributes.name,
      imgUrl: `/api/v1/gallery/${id}/cover`,
      linkUrl: `/g/${id}`,
      srcUrl: hits[i]._source.attributes.src,
      timestamp: getDatetime(hits[i]._source.timestamp),
    };
    items.push(item);
  }
  return items;
}

export default {
  components: { PreviewList },
  setup() {
    const route = useRoute();
    const previews = reactive<Previews>({
      pagination: undefined,
      items: undefined,
    });

    function load() {
      const searchQuery = JSON.parse(JSON.stringify(route.query)) as SearchQuery;
      if (searchQuery.size === undefined) {
        searchQuery.size = userState.frontSetting.gallery_preview_size;
      }
      if (searchQuery.page === undefined) {
        searchQuery.page = 1;
      }

      if (searchQuery.size === undefined) {
        return;
      }

      let getQuery = getSearch;
      if (route.path === "/gallery/random") {
        getQuery = getRandom;
      } else if (route.path === "/gallery/advanced-search") {
        getQuery = getAdvancedSearch;
      }

      getQuery(searchQuery).then((response) => {
        const hits = response.data.hits.hits ? response.data.hits.hits : [];
        const totalItems = response.data.hits.total.value as number;

        previews.pagination = getPagination(route.path, totalItems, searchQuery);
        previews.items = getItems(hits);
      });
    }
    load();

    watch(
      () => {
        return [userState.frontSetting.gallery_preview_size, route.path, JSON.stringify(route.query)];
      },
      () => {
        load();
      },
    );
    return { previews };
  },
};
</script>
