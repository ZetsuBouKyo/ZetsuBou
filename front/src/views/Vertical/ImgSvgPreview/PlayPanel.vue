<template>
  <div class="hidden sm:block fixed right-0 top-20 m-4 bg-opacity-50 rounded-lg p-2">
    <div class="flex flex-col">
      <div class="flex flex-col" v-if="state.bookmark !== undefined && state.current !== undefined">
        <icon-mdi-bookmark-outline
          class="cursor-pointer hover:opacity-50 opacity-100 my-2"
          style="font-size: 1.5rem; color: white"
          v-if="!state.isBookmark"
          @click="addBookmark" />
        <icon-mdi-bookmark
          class="cursor-pointer hover:opacity-50 opacity-100 my-2"
          style="font-size: 1.5rem; color: white"
          v-else
          @click="deleteBookmark" />
      </div>
      <icon-mdi-file-edit-outline
        class="cursor-pointer hover:opacity-50 opacity-100 my-2"
        style="font-size: 1.5rem; color: white"
        @click="tagger.toggleTagger" />
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
      <span :key="state.current" v-if="state.current !== undefined">
        {{ state.current + 1 }} / {{ state.imgs.length }}
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
        v-if="!state.isPlay" />
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

<script lang="ts">
import { useRoute, useRouter } from "vue-router";
import { reactive, onMounted, onBeforeMount, watch } from "vue";

import { getImages } from "@/api/v1/gallery/image";
import {
  getUserBookmarkGallery,
  postUserBookmarkGallery,
  putUserBookmarkGallery,
  deleteUserBookmarkGallery,
} from "@/api/v1/user/bookmark/gallery";

import { userState } from "@/state/user";

interface Bookmark {
  user_id: number;
  gallery_id: string;
  page: number;
  [key: string]: any;
}

interface State {
  bookmark: undefined | null | Bookmark;
  current: number;
  isBookmark: boolean;
  [key: string]: any;
}

export default {
  props: {
    tagger: {
      type: Object,
      default: undefined,
    },
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();

    const tagger = props.tagger;

    const state = reactive<State>({
      imgs: [],
      gallery: route.params.gallery as any,
      imgName: route.params.img,
      timeInterval: route.query.interval ? parseInt(route.query.interval as string) : 5,
      current: undefined,
      isPlay: route.query.play as any,
      play: undefined,
      bookmark: undefined,
      isBookmark: false,
    });

    function updateBookmarkStatus() {
      if (state.current === undefined || state.bookmark === undefined) {
        return;
      }
      if (state.bookmark && state.bookmark.page === state.current) {
        state.isBookmark = true;
      } else {
        state.isBookmark = false;
      }
    }

    function checkCurrentPath() {
      const currentPath = route.path;
      const baseUrl = `/g/${state.gallery}/i/`;
      if (!currentPath.startsWith(baseUrl)) {
        clearInterval(state.play);
      }
    }

    watch(
      () => {
        return [JSON.stringify(route.params), JSON.stringify(route.query)];
      },
      () => {
        if (route.params.gallery !== undefined) {
          state.gallery = route.params.gallery;
        }
        if (route.params.imgName !== undefined) {
          state.imgName = route.params.imgName;
        }
        if (route.params.timeInterval !== undefined) {
          state.timeInterval = route.params.timeInterval as any;
        }
        checkCurrentPath();
      },
    );
    watch(
      () => {
        return [JSON.stringify(state.bookmark), state.current];
      },
      () => {
        updateBookmarkStatus();
      },
    );

    function back() {
      const url = "/g/" + state.gallery;
      router.push(url);
    }
    function getNextPageUrl() {
      const nextP = state.current + 1;
      let url = undefined;
      if (nextP < state.imgs.length) {
        url = `/g/${state.gallery}/i/${state.imgs[nextP]}`;
        state.current = nextP;
      }
      return url;
    }

    function previousPage() {
      const previousP = state.current - 1;
      if (previousP > -1) {
        const url = `/g/${state.gallery}/i/${state.imgs[previousP]}`;
        state.current = previousP;
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
      state.isPlay = true;
      if (state.current === state.imgs.length - 1) {
        state.isPlay = false;
        return;
      }
      state.play = setInterval(() => {
        const baseUrl = getNextPageUrl();
        if (baseUrl === undefined) {
          state.isPlay = false;
          clearInterval(state.play);
          return;
        }
        const url = `${baseUrl}?play=1&interval=${state.timeInterval.toString()}`;
        router.push(url);
      }, state.timeInterval * 1000);
    }

    function stopPlay() {
      clearTimeout(state.play);
      state.isPlay = false;
    }

    onBeforeMount(() => {
      document.addEventListener.call(window, "keyup", (event: any) => {
        if (event.keyCode === 39) {
          nextPage();
        } else if (event.keyCode === 37) {
          previousPage();
        }
      });
    });

    function load() {
      getImages(state.gallery).then((response) => {
        state.imgs = response.data;
        state.current = state.imgs.indexOf(state.imgName);
        if (state.isPlay) {
          startPlay();
        }
      });
    }

    onMounted(() => {
      load();
      loadBookmark();
    });

    function loadBookmark() {
      const userID = userState.id;
      const galleryID = route.params.gallery as string;
      getUserBookmarkGallery(userID, galleryID).then((response: any) => {
        state.bookmark = null;
        if (response.data) {
          state.bookmark = response.data;
        }
      });
    }

    function getNewBookmark() {
      const userID = userState.id;
      const galleryID = route.params.gallery as string;
      const page = state.current;
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

      const bookmark = state.bookmark;
      switch (bookmark) {
        case null:
          postUserBookmarkGallery(newBookmark.user_id, newBookmark).then((response: any) => {
            if (response.status === 200) {
              state.bookmark = response.data;
            }
          });
          break;
        case undefined:
          break;
        default:
          newBookmark.id = bookmark.id;
          putUserBookmarkGallery(newBookmark.user_id, newBookmark).then((response: any) => {
            if (response.status === 200) {
              state.bookmark = newBookmark;
            }
          });
      }
    }

    function deleteBookmark() {
      const userID = userState.id;
      const bookmark = state.bookmark;
      if (bookmark.id) {
        deleteUserBookmarkGallery(userID, bookmark.id).then((response: any) => {
          if (response.status === 200) {
            state.bookmark = null;
          }
        });
      }
    }

    return {
      addBookmark,
      back,
      deleteBookmark,
      nextPage,
      previousPage,
      startPlay,
      state,
      stopPlay,
      tagger,
    };
  },
};
</script>
