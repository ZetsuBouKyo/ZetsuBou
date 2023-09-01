<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { SearchBase, SearchQuery } from "@/interface/search";
import { SourceState } from "@/interface/source";
import { Video } from "@/interface/video";

import Labels from "@/components/Labels/index.vue";
import Tags from "@/components/Tags/index.vue";
import TextEditor from "@/components/TextEditor/index.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";
import StarRating from "@/elements/Rating/StarRating.vue";
import Editor from "./Editor.vue";

import { postVideoCreateCover } from "@/api/v1/task/airflow";
import { getAdvancedSearch, getRandom, getSearch } from "@/api/v1/video/query";

import { messageState } from "@/state/message";
import { userState } from "@/state/user";
import { videoState } from "@/state/video";

interface Item {
  title: string;
  rating: number;
  imgUrl: string;
  linkUrl: string;
}

interface State {
  items: Array<Item>;
}

const route = useRoute();

const state = reactive<State>({
  items: [],
});

watch(
  () => userState.data.frontSetting.video_preview_size,
  () => {
    const searchQuery = JSON.parse(JSON.stringify(route.query)) as SearchQuery;
    if (searchQuery.size === undefined) {
      searchQuery.size = userState.data.frontSetting.video_preview_size;
    }

    let getQuery = getSearch;
    if (searchQuery["search_base"] === SearchBase.Random) {
      getQuery = getRandom;
    } else if (searchQuery["search_base"] === SearchBase.AdvancedSearch) {
      getQuery = getAdvancedSearch;
    }

    const queryList = [];
    for (const key in searchQuery) {
      queryList.push(`${key}=${searchQuery[key]}`);
    }
    const queries = queryList.join("&");

    getQuery(searchQuery).then((response) => {
      const hits = response.data.hits.hits ? response.data.hits.hits : [];
      for (const hit of hits) {
        const video = hit._source as Video;
        state.items.push({
          title: video.name,
          rating: video.attributes.rating,
          imgUrl: `/api/v1/video/v/${video.id}/cover`,
          linkUrl: `/v/${video.id}?${queries}`,
        });
      }
    });
  },
);

const video = ref();
function makeCover() {
  const currentTime = video.value.currentTime;

  const videoID = videoState.data.id;
  const fps = videoState.data.attributes.fps;
  const frames = videoState.data.attributes.frames;
  const duration = frames / fps;
  let currentFrame = Math.floor((currentTime / duration) * frames);

  postVideoCreateCover(videoID, currentFrame).then((response: any) => {
    messageState.sendAirflowMessage(response, "Making Cover", "Successfully made cover", "Failed to make Cover");
  });
}

const textEditor = ref();
function openTextEditor() {
  textEditor.value.open();
}

const editor = ref();
function openEditor() {
  editor.value.open();
}

function onOverwrite(state: SourceState<Video>, data: Video) {
  if (data.name !== undefined) {
    state.data.name = data.name;
  }
  if (data.attributes !== undefined) {
    state.data.attributes = data.attributes;
  }
  if (data.tags !== undefined) {
    state.data.tags = data.tags;
  }
  if (data.labels !== undefined) {
    state.data.labels = data.labels;
  }
  if (data.other_names !== undefined && data.other_names.length > 0) {
    state.data.other_names = data.other_names;
  }
}
</script>

<template>
  <text-editor
    ref="textEditor"
    :title="'Video JSON Editor'"
    :state="videoState"
    :on-overwrite="onOverwrite"
    :save-message="'Video tag saved'"
    :reset-message="'Video tag is reset'" />
  <editor ref="editor" />
  <section class="body-font overflow-hidden lg:mx-8 mx-2">
    <div class="px-2 py-6 mx-auto" v-if="videoState.data">
      <div class="flex flex-row">
        <div class="flex flex-col flex-1">
          <video ref="video" class="h-70v w-full mb-4" controls v-if="videoState.data.id">
            <source :src="`/api/v1/video/v/${videoState.data.id}`" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <h3 class="text-gray-400 tracking-widest" v-if="videoState.data.attributes.category">
            {{ videoState.data.attributes.category }}
          </h3>
          <div class="flex flex-row items-center text-white 3xl:text-2xl text-xl font-medium mt-2 mb-1">
            <h1 class="lg:w-full w-80 hover:opacity-50 cursor-pointer break-all" v-if="videoState.data.name">
              {{ videoState.data.name }}
            </h1>
            <h1
              class="ml-auto w-32 text-right text-base text-gray-400 items-center"
              v-if="videoState.data.attributes.width && videoState.data.attributes.height">
              {{ videoState.data.attributes.width }} x {{ videoState.data.attributes.height }}
            </h1>
          </div>
          <!-- <div class="ml-auto 3xl:text-xl">
            <a class="text-gray-300" v-if="videoState.data.attributes.src" :href="videoState.data.attributes.src">{{
              videoState.data.attributes.src
            }}</a>
          </div> -->
          <div class="flex flex-col divide-y divide-gray-500">
            <div class="flex flex-col">
              <div class="flex flex-row my-4 mr-auto">
                <star-rating :filled="videoState.data.attributes.rating" />
              </div>
              <div class="flex flex-row-reverse">
                <ripple-button class="flex btn hover:opacity-50 hover:bg-gray-500">
                  <div class="inline-flex items-center" @click="openEditor">
                    <icon-ic-outline-edit class="m-1" style="font-size: 1.2rem; color: white" />
                    <span class="mr-2 text-white">Edit</span>
                  </div>
                </ripple-button>
                <ripple-button class="flex btn hover:opacity-50 hover:bg-gray-500">
                  <div class="inline-flex items-center" @click="openTextEditor">
                    <icon-mdi-code-json class="my-1 ml-1 mr-2" style="font-size: 1.2rem; color: white" />
                    <span class="mr-2 text-white">JSON</span>
                  </div>
                </ripple-button>
                <ripple-button class="flex btn hover:opacity-50 hover:bg-gray-500">
                  <div class="inline-flex items-center" @click="makeCover">
                    <icon-ic-baseline-photo-camera class="my-1 ml-1 mr-2" style="font-size: 1.2rem; color: white" />
                    <span class="mr-2 text-white">Make Cover</span>
                  </div>
                </ripple-button>
              </div>
              <labels
                v-if="videoState.data.labels && videoState.data.labels.length > 0"
                class="mb-2"
                :labels="videoState.data.labels"
                :searchBaseUrl="'/video/advanced-search'" />
              <tags class="ml-2" :tags="videoState.data.tags" :searchBaseUrl="'/video/advanced-search'" />
            </div>
          </div>
        </div>
        <div class="lg:flex lg:flex-col hidden w-80 ml-4">
          <div class="flex flex-row mb-2">
            <span class="flex-initial text-white rounded-full px-4 py-2 border-1 border-white bg-gray-900"
              >From your search</span
            >
          </div>
          <div class="flex flex-row py-2 h-36" v-for="(item, i) in state.items" :key="i">
            <div class="flex h-full flex-1">
              <a :href="item.linkUrl" class="w-full">
                <img
                  alt="Not found!"
                  loading="lazy"
                  class="object-contain object-center w-full h-full block animate-fade-in"
                  :src="item.imgUrl" />
              </a>
            </div>
            <div class="flex flex-col w-40 ml-2 self-center">
              <a class="w-full" :href="item.linkUrl">
                <span class="text-white w-full truncate">{{ item.title }}</span>
              </a>
              <star-rating class="mt-2" :filled="item.rating" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
