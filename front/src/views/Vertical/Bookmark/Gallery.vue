<template>
  <div class="views-setting-container">
    <div
      class="flex flex-col w-full mx-auto rounded-lg overflow-x-auto bg-gray-800 shadow-gray-900 scrollbar-gray-900-2"
      :class="state.rows.length ? 'divide-y divide-gray-500' : ''"
      :key="state.uuid">
      <div class="flex flex-row w-full p-4 cursor-default" v-if="state.rows.length === 0">
        <div class="flex flex-row w-full">
          <span class="w-24 self-center mr-2">No results</span>
        </div>
      </div>
      <div
        class="flex flex-row w-full p-4"
        v-for="(row, i) in state.rows"
        :key="i + state.rows.length + JSON.stringify(row)">
        <div class="flex flex-row w-full hover:opacity-50">
          <span class="w-12 self-center mr-2">{{ i + 1 }}</span>
          <div class="flex h-36 w-24">
            <img
              alt="Not found!"
              loading="lazy"
              class="object-contain object-center h-full w-full animate-fade-in"
              :src="getCover(row)" />
          </div>
          <div class="flex flex-col w-full mx-4">
            <span class="text-gray-400 text-xs" v-if="row.gallery.attributes.category">{{
              row.gallery.attributes.category
            }}</span>
            <div class="flex flex-row">
              <router-link class="text-white text-base cursor-pointer" :to="toGallery(row)">
                {{ row.gallery.attributes.name }}
              </router-link>
              <span class="ml-auto text-gray-400 text-xs w-24">page: {{ row.bookmark.page + 1 }}</span>
            </div>
            <span class="text-gray-500 text-sm my-1 truncate" v-if="row.gallery.attributes.raw_name">{{
              row.gallery.attributes.raw_name
            }}</span>
            <star-rating class="my-2" :filled="row.gallery.attributes.rating" />
            <span class="mt-auto ml-auto">last viewed: {{ getDatetime(row.bookmark.modified) }}</span>
          </div>
        </div>
        <div class="flex flex-col ml-auto" :key="JSON.stringify(row)">
          <ripple-button
            class="h-10 mr-2 btn-icon cursor-pointer"
            :class="ButtonColorEnum.Primary"
            @click="toBookmark(row)">
            <div class="ml-2"><icon-mdi-arrow /></div>
            <span class="ml-2 mr-4">Go</span>
          </ripple-button>
          <ripple-button
            class="h-10 mt-2 mr-2 btn-icon cursor-pointer"
            :class="ButtonColorEnum.Danger"
            @click="deleteBookmark(row)">
            <div class="ml-2"><icon-mdi-trash-can-outline /></div>
            <span class="ml-2 mr-4">Delete</span>
          </ripple-button>
        </div>
      </div>
      <div class="flex flex-row">
        <pagination-base
          class="ml-auto mr-4"
          v-if="state.pagination"
          :pagination="state.pagination"
          :key="state.pagination.current" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { reactive, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { ButtonColorEnum } from "@/elements/Button/button";
import { GetParam } from "@/elements/Table/CrudTable/index.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";
import StarRating from "@/elements/Rating/StarRating.vue";
import { getPagination } from "@/elements/Pagination/pagination";
import PaginationBase from "@/elements/Pagination/index.vue";

import {
  getUserTotalBookmarks,
  getUserDetailedGalleryBookmarks,
  deleteUserBookmarkGallery,
} from "@/api/v1/user/bookmark/gallery";
import { getImages } from "@/api/v1/gallery/image";

import { userState } from "@/state/user";
import { messageState } from "@/state/message";

import { Gallery } from "@/interface/gallery";
import { Pagination } from "@/elements/Pagination/interface";

import { getDatetime } from "@/utils/datetime";
import { getUUID } from "@/utils/str";
import { detectRouteChange } from "@/utils/route";

interface Bookmark {
  id: number;
  user_id: number;
  gallery_id: string;
  page: number;
  modified: string;
}

export interface Row {
  bookmark: Bookmark;
  gallery: Gallery;
}

interface State {
  uuid: string;
  userID: number;
  pagination: Pagination;
  rows: Array<Row>;
}

export default {
  components: { PaginationBase, RippleButton, StarRating },
  setup() {
    const state = reactive<State>({
      uuid: getUUID(),
      userID: undefined,
      pagination: undefined,
      rows: [],
    });
    const router = useRouter();
    const route = useRoute();
    const params: GetParam = {
      page: undefined,
      size: undefined,
      is_desc: undefined,
    };

    function updateParams() {
      params.page = route.query.page ? parseInt(route.query.page as string) : 1;
      params.size = route.query.size ? parseInt(route.query.size as string) : 20;
      params.is_desc = route.query.is_desc ? Boolean(route.query.is_desc) : true;
    }

    state.userID = userState.id;

    function load() {
      updateParams();
      axios.all<any>([getUserTotalBookmarks(state.userID), getUserDetailedGalleryBookmarks(state.userID, params)]).then(
        axios.spread((response1, response2) => {
          const totalItems = response1.data;
          const rows = response2.data;
          state.pagination = getPagination(route.path, totalItems, params);
          state.rows = rows;
          state.uuid = getUUID();
        }),
      );
    }
    load();

    watch(
      () => detectRouteChange(route),
      () => {
        load();
      },
    );

    function getCover(row: Row) {
      const galleryID = row.bookmark.gallery_id;
      return `/api/v1/gallery/${galleryID}/cover`;
    }

    function toGallery(row: Row) {
      const galleryID = row.bookmark.gallery_id;
      return `/g/${galleryID}`;
    }

    function deleteBookmark(row: Row) {
      const bookmarkID = row.bookmark.id;
      if (state.userID === undefined || bookmarkID === undefined) {
        return;
      }
      deleteUserBookmarkGallery(state.userID, bookmarkID).then((response) => {
        if (response.status === 200) {
          messageState.push("Deleted bookmark");
          load();
        }
      });
    }

    function toBookmark(row: Row) {
      const galleryID = row.bookmark.gallery_id;
      getImages(galleryID).then((response) => {
        const imgs = response.data;
        const imgName = imgs[row.bookmark.page];
        const url = `/g/${galleryID}/i/${imgName}`;
        router.push(url);
      });
    }

    return {
      state,
      route,
      ButtonColorEnum,
      getCover,
      toGallery,
      toBookmark,
      getDatetime,
      deleteBookmark,
      detectRouteChange,
    };
  },
};
</script>
