<template>
  <text-editor
    ref="textEditor"
    :title="'Gallery JSON Editor'"
    :state="galleryState"
    :on-overwrite="onOverwrite"
    :save-message="'Gallery tag saved'"
    :reset-message="'Gallery tag is reset'" />
  <editor ref="editor" />
  <section class="body-font overflow-hidden lg:mx-8 mx-2">
    <div class="px-2 py-6 mx-auto">
      <div class="md:w-full mx-auto flex flex-wrap w-full" v-if="galleryState.data">
        <img
          alt="ecommerce"
          class="lg:w-1/2 lg:h-70v w-full object-contain object-center rounded-lg border-2 border-gray-600 px-6 py-6 animate-fade-in"
          :src="cover" />
        <div class="lg:w-1/2 lg:pl-10 lg:mt-0 lg:h-70v w-full mt-6 flex flex-col">
          <h3 class="text-gray-500 3xl:text-xl text-xs tracking-widest" v-if="galleryState.data.attributes.category">
            {{ galleryState.data.attributes.category }}
          </h3>
          <h1
            class="hover:opacity-50 text-white 3xl:text-2xl text-xl font-medium mb-1 cursor-pointer"
            v-if="galleryState.data.attributes.name"
            @click="copy">
            {{ galleryState.data.attributes.name }}
          </h1>
          <h2
            class="hover:opacity-50 3xl:text-xl text-sm text-gray-500 tracking-widest cursor-pointer"
            v-if="galleryState.data.attributes.raw_name"
            @click="copy">
            {{ galleryState.data.attributes.raw_name }}
          </h2>
          <div class="flex flex-row mt-4 mb-2 justify-center items-center">
            <star-rating :filled="galleryState.data.attributes.rating" />
            <div class="flex ml-auto 3xl:text-xl">
              <a v-if="galleryState.data.attributes.src" :href="galleryState.data.attributes.src">{{
                galleryState.data.attributes.src
              }}</a>
            </div>
          </div>
          <h3 class="text-gray-500 3xl:text-xl text-xs tracking-widest ml-auto mb-4" v-if="galleryState.data.timestamp">
            Last updated on {{ galleryState.getTimestamp() }}
          </h3>
          <labels
            v-if="galleryState.data.labels && galleryState.data.labels.length > 0"
            class="mb-2 lg:h-1/4 rounded-lg border-2 border-gray-600 lg:overflow-y-scroll lg:scrollbar-gray-100-2"
            :labels="galleryState.data.labels"
            :searchBaseUrl="'/gallery/advanced-search'" />
          <tags
            class="px-2 lg:overflow-y-scroll lg:scrollbar-gray-100-2 lg:h-full rounded-lg border-2 border-gray-600"
            :tags="galleryState.data.tags"
            :searchBaseUrl="'/gallery/advanced-search'" />
          <control-panel :state="controlPanelState" />
        </div>
      </div>
      <div class="md:w-full mx-auto flex flex-wrap w-full animate-pulse" v-else>
        <div
          class="lg:w-1/2 lg:h-70v w-full object-contain object-center rounded-lg border-2 border-gray-600 px-6 py-6 animate-fade-in"></div>
        <div class="lg:w-1/2 lg:pl-10 lg:mt-0 lg:h-70v w-full mt-6 flex flex-col"></div>
      </div>
    </div>
    <confirm-modal
      ref="confirmDelete"
      :title="'Warning'"
      :message="'Do you really want to delete this gallery?'"
      :on-confirm="onConfirmDelete" />
  </section>
</template>

<script lang="ts">
import { onBeforeMount, reactive, ref } from "vue";
import { useRoute } from "vue-router";

import { deleteGalleryByID } from "@/api/v1/gallery/operation";
import { getTaskStandaloneGalleryOpen } from "@/api/v1/task/standalone";

import ConfirmModal from "@/elements/Modal/ConfirmModal.vue";
import StarRating from "@/elements/Rating/StarRating.vue";

import Labels from "@/components/Labels/index.vue";
import Tags from "@/components/Tags/index.vue";
import TextEditor from "@/components/TextEditor/index.vue";
import ControlPanel from "./ControlPanel.vue";
import Editor from "./Editor.vue";

import { galleryState } from "@/state/gallery";

import { ControlPanelState } from "./ControlPanel.d";

import { Gallery } from "@/interface/gallery";
import { SourceState } from "@/interface/source";

export default {
  components: { StarRating, Labels, Tags, ControlPanel, TextEditor, Editor, ConfirmModal },
  setup() {
    const route = useRoute();
    const id = route.params.gallery as string;

    onBeforeMount(() => {
      galleryState.init(id);
    });

    const confirmDelete = ref();
    const editor = ref();
    const textEditor = ref();

    function onOpenConfirmDelete() {
      confirmDelete.value.open();
    }

    function openEditor() {
      editor.value.open();
    }

    function openTextEditor() {
      textEditor.value.open();
    }

    function onConfirmDelete() {
      deleteGalleryByID(id).then(() => {
        if (window.history.back() === undefined) {
          window.close();
        }
      });
    }

    const controlPanelState = reactive<ControlPanelState>({
      openGallery: () => {
        getTaskStandaloneGalleryOpen(id).then(() => {});
      },
      openEditor: openEditor,
      openTextEditor: openTextEditor,
      openConfirmDeleteMessage: onOpenConfirmDelete,
    });

    function copy(event) {
      navigator.clipboard.writeText(event.target.textContent);
    }

    const cover = `/api/v1/gallery/${id}/cover`;

    function onOverwrite(state: SourceState<Gallery>, data: Gallery) {
      if (data.attributes !== undefined) {
        state.data.attributes = data.attributes;
      }
      if (data.tags !== undefined) {
        state.data.tags = data.tags;
      }
      if (data.labels !== undefined) {
        state.data.labels = data.labels;
      }
    }

    return {
      cover,
      galleryState,
      confirmDelete,
      editor,
      textEditor,
      onConfirmDelete,
      onOverwrite,
      controlPanelState,
      copy,
    };
  },
};
</script>
