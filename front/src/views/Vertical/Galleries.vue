<script setup lang="ts">
import { reactive } from "vue";
import { useRoute } from "vue-router";

import { Item, Items, Previews } from "@/components/PreviewList/interface";
import { SearchQuery } from "@/interface/search";

import PreviewList from "@/components/PreviewList/index.vue";

import { getAdvancedSearch, getRandom, getSearch } from "@/api/v1/gallery/query";

import { routeState } from "@/state/route";
import { userState } from "@/state/user";

import { getPagination } from "@/elements/Pagination/pagination";
import { getDatetime } from "@/utils/datetime";

function getItems(hits: any) {
  let items: Items = [];
  for (let i = 0; i < hits.length; i++) {
    let id = hits[i]._id;

    const src = hits[i]._source.src ? hits[i]._source.src[0] : undefined;

    let item: Item = {
      category: hits[i]._source.attributes.category,
      rating: hits[i]._source.attributes.rating,
      title: hits[i]._source.name,
      imgUrl: `/api/v1/gallery/${id}/cover`,
      linkUrl: `/g/${id}`,
      srcUrl: src,
      lastUpdated: getDatetime(hits[i]._source.last_updated),
    };
    const pages = hits[i]._source?.attributes?.pages;
    if (pages !== undefined) {
      item.pages = pages;
    }
    items.push(item);
  }
  return items;
}

const route = useRoute();
const previews = reactive<Previews>({
  pagination: undefined,
  items: undefined,
});

function load() {
  const searchQuery = JSON.parse(JSON.stringify(route.query)) as SearchQuery;
  if (searchQuery.size === undefined) {
    searchQuery.size = userState.data.frontSetting.gallery_preview_size;
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

function watchSources() {
  return userState.data.frontSetting.gallery_preview_size;
}

routeState.setRoute(route);
routeState.setWatchSources(watchSources);
routeState.setLoadFunction(load);
</script>

<template>
  <div>
    <preview-list :previews="previews" />
  </div>
</template>
