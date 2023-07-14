<script setup lang="ts">
import { reactive, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { Item, Items, Previews } from "@/components/PreviewList/interface";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";

import PreviewList from "@/components/PreviewList/index.vue";
import Info from "./Info/index.vue";

import { getImages } from "@/api/v1/gallery/image";

import { userState } from "@/state/user";

import { getPagination } from "@/elements/Pagination/pagination";

function getItems(id: string, data: any, query: PaginationGetParam) {
  const items: Items = [];
  const page = query.page as number;
  const size = query.size as number;
  for (let i = (page - 1) * size; i < data.length && i < page * size; i++) {
    let item: Item = {
      imgUrl: `/api/v1/gallery/${id}/i/${data[i]}`,
      linkUrl: `/g/${id}/i/${data[i]}`,
    };
    items.push(item);
  }
  return items;
}

const route = useRoute();
const router = useRouter();
const id = route.params.gallery as string;

const previews = reactive<Previews>({
  pagination: undefined,
  items: undefined,
});

function load() {
  if (userState.frontSetting.img_preview_size === undefined) {
    return;
  }
  const page = parseInt(route.query.page as string);
  const query: PaginationGetParam = {
    page: page ? page : 1,
    size: userState.frontSetting.img_preview_size,
  };

  getImages(id)
    .then((response) => {
      const imgs = response.data;
      const total = imgs.length;

      previews.pagination = getPagination(route.path, total, query);
      previews.items = getItems(id, imgs, query);
    })
    .catch(() => {
      router.push("/NotFound");
    });
}
load();

watch(
  () => {
    return [userState.frontSetting.img_preview_size, JSON.stringify(route.path), JSON.stringify(route.query.page)];
  },
  () => {
    load();
  },
);
</script>

<template>
  <div class="divide-y divide-gray-500">
    <info />
    <preview-list :previews="previews" />
  </div>
</template>
