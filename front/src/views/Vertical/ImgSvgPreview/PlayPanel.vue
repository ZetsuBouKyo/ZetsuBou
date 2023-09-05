<script setup lang="ts">
import { PropType, onBeforeMount, onBeforeUnmount, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { getImages } from "@/api/v1/gallery/image";
import {
  deleteUserBookmarkGallery,
  getUserBookmarkGallery,
  postUserBookmarkGallery,
  putUserBookmarkGallery,
} from "@/api/v1/user/bookmark/gallery";

import { userState } from "@/state/user";

import { SVG } from "./SvgEditor/svg.interface";

const props = defineProps({
  svg: {
    type: Object as PropType<SVG>,
    required: true,
  },
});

const route = useRoute();
const router = useRouter();

const svgState = props.svg;

function updateBookmarkStatus() {
  if (svgState.panel.current === undefined || svgState.bookmark === undefined) {
    return;
  }
  if (svgState.bookmark) {
    if (svgState.bookmark.page === svgState.panel.current) {
      svgState.bookmark.isBookmark = true;
    } else {
      svgState.bookmark.isBookmark = false;
    }
  }
}

function checkCurrentPath() {
  const currentPath = route.path;
  const baseUrl = `/g/${svgState.panel.galleryID}/i/`;
  if (!currentPath.startsWith(baseUrl)) {
    clearInterval(svgState.panel.play);
  }
}

watch(
  () => {
    return [JSON.stringify(route.params), JSON.stringify(route.query)];
  },
  () => {
    if (route.params.gallery !== undefined) {
      svgState.panel.galleryID = route.params.gallery as string;
    }
    if (route.params.imgName !== undefined) {
      svgState.panel.imgName = route.params.imgName as string;
    }
    if (route.params.timeInterval !== undefined) {
      svgState.panel.timeInterval = parseInt(route.params.timeInterval as string) as number;
    }
    checkCurrentPath();
  },
);
watch(
  () => {
    return [JSON.stringify(svgState.bookmark), svgState.panel.current];
  },
  () => {
    updateBookmarkStatus();
  },
);

function back() {
  const url = "/g/" + svgState.panel.galleryID;
  router.push(url);
}
function getNextPageUrl() {
  const nextP = svgState.panel.current + 1;
  let url = undefined;
  if (nextP < svgState.panel.imgs.length) {
    url = `/g/${svgState.panel.galleryID}/i/${svgState.panel.imgs[nextP]}`;
    svgState.panel.current = nextP;
  }
  return url;
}

function previousPage() {
  const previousP = svgState.panel.current - 1;
  if (previousP > -1) {
    const url = `/g/${svgState.panel.galleryID}/i/${svgState.panel.imgs[previousP]}`;
    svgState.panel.current = previousP;
    router.push(url);
  }
}

function nextPage() {
  const url = getNextPageUrl();
  if (url !== undefined) {
    router.push(url);
  }
}

function startPlay() {
  svgState.panel.isPlay = true;
  if (svgState.panel.current === svgState.panel.imgs.length - 1) {
    svgState.panel.isPlay = false;
    return;
  }
  svgState.panel.play = setInterval(() => {
    const baseUrl = getNextPageUrl();
    if (baseUrl === undefined) {
      svgState.panel.isPlay = false;
      clearInterval(svgState.panel.play);
      return;
    }
    const url = `${baseUrl}?play=1&interval=${svgState.panel.timeInterval.toString()}`;
    router.push(url);
  }, svgState.panel.timeInterval * 1000);
}

function stopPlay() {
  clearTimeout(svgState.panel.play);
  svgState.panel.isPlay = false;
}

function onPage(event: any) {
  if (event.keyCode === 39) {
    nextPage();
  } else if (event.keyCode === 37) {
    previousPage();
  }
}

onBeforeMount(() => {
  window.addEventListener("keyup", onPage);
});

onBeforeUnmount(() => {
  window.removeEventListener("keyup", onPage);
});

function load() {
  getImages(svgState.panel.galleryID).then((response) => {
    svgState.panel.imgs = response.data;
    svgState.panel.current = svgState.panel.imgs.indexOf(svgState.panel.imgName as never);
    if (svgState.panel.isPlay) {
      startPlay();
    }
  });
}

onMounted(() => {
  load();
  loadBookmark();
});

function loadBookmark() {
  const userID = userState.data.id;
  const galleryID = route.params.gallery as string;
  getUserBookmarkGallery(userID, galleryID).then((response: any) => {
    svgState.bookmark = null;
    if (response.data) {
      svgState.bookmark = response.data;
    }
  });
}

function getNewBookmark() {
  const userID = userState.data.id;
  const galleryID = route.params.gallery as string;
  const page = svgState.panel.current;
  if (userID === undefined || galleryID === undefined || page === undefined) {
    return undefined;
  }
  return {
    user_id: userID,
    gallery_id: galleryID,
    page: page,
  };
}

function addBookmark() {
  const newBookmark = getNewBookmark() as any;
  if (newBookmark === undefined) {
    return;
  }

  const bookmark = svgState.bookmark;
  switch (bookmark) {
    case null:
      postUserBookmarkGallery(newBookmark.user_id, newBookmark).then((response: any) => {
        if (response.status === 200) {
          svgState.bookmark = response.data;
        }
      });
      break;
    case undefined:
      break;
    default:
      newBookmark.id = bookmark.id;
      putUserBookmarkGallery(newBookmark.user_id, newBookmark).then((response: any) => {
        if (response.status === 200) {
          svgState.bookmark = newBookmark;
        }
      });
  }
}

function deleteBookmark() {
  const userID = userState.data.id;
  const bookmark = svgState.bookmark;
  if (bookmark.id) {
    deleteUserBookmarkGallery(userID, bookmark.id).then((response: any) => {
      if (response.status === 200) {
        svgState.bookmark = null;
      }
    });
  }
}
</script>

<template>
  <div class="hidden sm:block fixed right-0 top-20 m-4 bg-opacity-50 rounded-lg p-2">
    <div class="flex flex-col">
      <div class="flex flex-col" v-if="svgState.bookmark !== undefined && svgState.panel.current !== undefined">
        <icon-mdi-bookmark
          class="cursor-pointer hover:opacity-50 opacity-100 my-2"
          style="font-size: 1.5rem; color: white"
          v-if="svgState.bookmark && svgState.bookmark.isBookmark"
          @click="deleteBookmark" />
        <icon-mdi-bookmark-outline
          class="cursor-pointer hover:opacity-50 opacity-100 my-2"
          style="font-size: 1.5rem; color: white"
          v-else
          @click="addBookmark" />
      </div>
      <icon-mdi-file-edit-outline
        class="cursor-pointer hover:opacity-50 opacity-100 my-2"
        style="font-size: 1.5rem; color: white"
        @click="svgState.sidebar.toggleSidebar" />
    </div>
  </div>
  <div class="fixed left-0 bottom-3 bg-gray-900 bg-opacity-50 rounded-lg m-1 p-1 flex">
    <icon-ri-arrow-go-back-fill
      class="cursor-pointer hover:opacity-50 opacity-100"
      style="font-size: 1.5rem; color: white"
      @click="back" />
  </div>
  <div class="flex flex-col fixed right-0 bottom-0 m-4 bg-gray-900 bg-opacity-50 rounded-lg p-2">
    <div class="flex mx-auto text-white">
      <span :key="svgState.panel.current" v-if="svgState.panel.current !== undefined">
        {{ svgState.panel.current + 1 }} / {{ svgState.panel.imgs.length }}
      </span>
      <span v-else>&emsp;</span>
    </div>
    <div class="flex">
      <icon-ic-round-keyboard-arrow-left
        class="cursor-pointer hover:opacity-50"
        style="font-size: 2rem; color: white"
        @click="previousPage" />
      <icon-ic-sharp-play-circle-filled
        class="cursor-pointer hover:opacity-50"
        style="font-size: 2rem; color: white"
        @click="startPlay"
        v-if="!svgState.panel.isPlay" />
      <icon-ic-round-stop-circle
        class="cursor-pointer hover:opacity-50"
        style="font-size: 2rem; color: white"
        @click="stopPlay"
        v-else />
      <icon-ic-round-keyboard-arrow-right
        class="cursor-pointer hover:opacity-50"
        style="font-size: 2rem; color: white"
        @click="nextPage" />
    </div>
  </div>
</template>
