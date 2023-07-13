<template>
  <div>
    <preview-list :previews="previews" />
  </div>
</template>

<script lang="ts">
import { reactive, watch } from "vue";
import { useRoute } from "vue-router";

import { getDatetime } from "@/utils/datetime";

import { getAdvancedSearch, getRandom, getSearch } from "@/api/v1/video/query";

import { userState } from "@/state/user";

import { Item, Items, Previews } from "@/components/PreviewList/interface";
import { SearchQuery } from "@/interface/search";

import { getPagination } from "@/elements/Pagination/pagination";

import PreviewList from "@/components/PreviewList/index.vue";

function getItems(hits: any, queries: string) {
  let items: Items = [];
  for (let i = 0; i < hits.length; i++) {
    let id = hits[i]._id;
    let item: Item = {
      category: hits[i]._source.attributes.category,
      rating: hits[i]._source.attributes.rating,
      title: hits[i]._source.name,
      imgUrl: `/api/v1/video/v/${id}/cover`,
      linkUrl: `/v/${id}?${queries}`,
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
        searchQuery.size = userState.frontSetting.video_preview_size;
      }
      if (searchQuery.page === undefined) {
        searchQuery.page = 1;
      }

      let getQuery = getSearch;
      if (route.path === "/video/random") {
        getQuery = getRandom;
      } else if (route.path === "/video/advanced-search") {
        getQuery = getAdvancedSearch;
      }

      const queryList = [];
      for (const key in searchQuery) {
        queryList.push(`${key}=${searchQuery[key]}`);
      }
      const queries = queryList.join("&");

      getQuery(searchQuery).then((response) => {
        const hits = response.data.hits.hits ? response.data.hits.hits : [];
        const totalItems = response.data.hits.total.value as number;

        previews.pagination = getPagination(route.path, totalItems, searchQuery);
        previews.items = getItems(hits, queries);
      });
    }
    load();

    watch(
      () => {
        return [userState.frontSetting.video_preview_size, route.path, JSON.stringify(route.query)];
      },
      () => {
        load();
      },
    );
    return { previews };
  },
};
</script>
