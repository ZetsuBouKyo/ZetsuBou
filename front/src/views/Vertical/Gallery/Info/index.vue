<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRoute } from "vue-router";

import { Gallery } from "@/interface/gallery";
import { SourceState } from "@/interface/state";
import { ControlPanelState } from "./ControlPanel.interface";

import Editor from "@/components/Editor/index.vue";
import Labels from "@/components/Labels/index.vue";
import Tags from "@/components/Tags/index.vue";
import TextEditor from "@/components/TextEditor/index.vue";
import ConfirmModal from "@/elements/Modal/ConfirmModal.vue";
import Rating from "@/elements/Rating/index.vue";
import ControlPanel from "./ControlPanel.vue";

import { deleteGalleryByID } from "@/api/v1/gallery/operation";
import {
    getSettingFrontGalleryStartsWithCategories,
    getSettingFrontGalleryStartsWithTagFields,
} from "@/api/v1/setting/front/gallery";
import { getTaskStandaloneGalleryOpen } from "@/api/v1/task/standalone";

import { galleryState } from "@/state/gallery";
import { messageState } from "@/state/message";

const route = useRoute();
const id = route.params.gallery as string;

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

function copy(event: any) {
    navigator.clipboard.writeText(event.target.textContent);
    messageState.push("Copied");
}

const cover = `/api/v1/gallery/${id}/cover`;

function onOverwrite(state: SourceState<Gallery>, data: Gallery) {
    if (data.name !== undefined) {
        state.data.name = data.name;
    }
    if (data.raw_name !== undefined) {
        state.data.raw_name = data.raw_name;
    }
    if (data.other_names !== undefined && data.other_names instanceof Array) {
        state.data.other_names = data.other_names;
    }
    if (data.src !== undefined && data.src instanceof Array) {
        state.data.src = data.src;
    }

    if (data.publication_date !== undefined) {
        state.data.publication_date = data.publication_date;
    }

    if (data.labels !== undefined) {
        state.data.labels = data.labels;
    }
    if (data.tags !== undefined) {
        state.data.tags = data.tags;
    }

    if (data.attributes !== undefined) {
        state.data.attributes = data.attributes;
    }
}
</script>

<template>
    <text-editor
        ref="textEditor"
        :title="'Gallery JSON Editor'"
        :state="galleryState"
        :on-overwrite="onOverwrite"
        :save-message="'Gallery tag saved'"
        :reset-message="'Gallery tag is reset'"
    />
    <editor
        ref="editor"
        :state="galleryState"
        :title="'Gallery Editor'"
        :saved-message="'Gallery tag saved'"
        :on-get-category-starts-with="getSettingFrontGalleryStartsWithCategories"
        :on-get-tag-field-starts-with="getSettingFrontGalleryStartsWithTagFields"
    />
    <section class="body-font overflow-hidden lg:mx-8 mx-2">
        <div class="px-2 py-6 mx-auto">
            <div class="md:w-full mx-auto flex flex-wrap w-full" v-if="galleryState.data">
                <img
                    alt="ecommerce"
                    class="lg:w-1/2 lg:h-70v w-full object-contain object-center rounded-lg border-2 border-gray-600 px-6 py-6 animate-fade-in"
                    :src="cover"
                />
                <div class="lg:w-1/2 lg:pl-10 lg:mt-0 lg:h-70v w-full mt-6 flex flex-col">
                    <h3
                        class="text-gray-500 3xl:text-xl text-xs tracking-widest"
                        v-if="galleryState.data.attributes.category"
                    >
                        {{ galleryState.data.attributes.category }}
                    </h3>
                    <h1
                        class="hover:opacity-50 text-white 3xl:text-2xl text-xl font-medium mb-1 cursor-pointer"
                        v-if="galleryState.data.name"
                        @click="copy"
                    >
                        {{ galleryState.data.name }}
                    </h1>
                    <h2
                        class="hover:opacity-50 3xl:text-xl text-sm text-gray-500 tracking-widest cursor-pointer"
                        v-if="galleryState.data.raw_name"
                        @click="copy"
                    >
                        {{ galleryState.data.raw_name }}
                    </h2>
                    <div class="flex flex-row mt-2 justify-center items-center">
                        <rating class="mr-auto" :filled="galleryState.data.attributes.rating" />
                    </div>
                    <div class="flex flex-col my-2 justify-center items-center max-h-12">
                        <a
                            class="flex ml-auto 3xl:text-xl"
                            v-if="galleryState.data.src.length > 0"
                            :href="galleryState.data.src[0]"
                        >
                            {{ galleryState.data.src[0] }}
                        </a>
                    </div>
                    <h3
                        class="text-gray-500 3xl:text-xl text-xs tracking-widest ml-auto mb-4"
                        v-if="galleryState.data.last_updated"
                    >
                        Last updated on {{ galleryState.getLastUpdated() }}
                    </h3>
                    <labels
                        v-if="galleryState.data.labels && galleryState.data.labels.length > 0"
                        class="mb-2 lg:h-1/4 rounded-lg border-2 border-gray-600 lg:overflow-y-scroll lg:scrollbar-gray-100-2"
                        :labels="galleryState.data.labels"
                        :searchBaseUrl="'/gallery/advanced-search'"
                    />
                    <tags
                        class="px-2 lg:overflow-y-scroll lg:scrollbar-gray-100-2 lg:h-full rounded-lg border-2 border-gray-600"
                        :tags="galleryState.data.tags"
                        :searchBaseUrl="'/gallery/advanced-search'"
                    />
                    <control-panel :state="controlPanelState" />
                </div>
            </div>
            <div class="md:w-full mx-auto flex flex-wrap w-full animate-pulse" v-else>
                <div
                    class="lg:w-1/2 lg:h-70v w-full object-contain object-center rounded-lg border-2 border-gray-600 px-6 py-6 animate-fade-in"
                ></div>
                <div class="lg:w-1/2 lg:pl-10 lg:mt-0 lg:h-70v w-full mt-6 flex flex-col"></div>
            </div>
        </div>
        <confirm-modal
            ref="confirmDelete"
            :title="'Warning'"
            :message="'Do you really want to delete this gallery?'"
            :on-confirm="onConfirmDelete"
        />
    </section>
</template>
