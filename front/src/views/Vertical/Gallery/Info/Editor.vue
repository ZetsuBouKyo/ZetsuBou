<template>
  <modal ref="editor" :title="'Gallery Editor'" class="w-1/2 top-12 left-1/4">
    <div class="modal-row-10">
      <span class="w-32 mr-4">Name:</span>
      <input
        class="flex-1 modal-input"
        type="text"
        :placeholder="galleryState.data.attributes.name"
        v-model="galleryState.data.attributes.name" />
    </div>
    <div class="modal-row-10">
      <span class="w-32 mr-4">Raw Name:</span>
      <input
        class="flex-1 modal-input"
        type="text"
        :placeholder="galleryState.data.attributes.raw_name"
        v-model="galleryState.data.attributes.raw_name" />
    </div>
    <div class="modal-row-10">
      <span class="w-32 mr-4">Source:</span>
      <input
        class="flex-1 modal-input"
        type="text"
        :placeholder="galleryState.data.attributes.src"
        v-model="galleryState.data.attributes.src" />
    </div>
    <div class="modal-row-10">
      <span class="w-32 mr-4">Category:</span>
      <select-dropdown
        class="w-64"
        :options-width-class="'w-64'"
        :state="category"
        :on-get="getSettingFrontGalleryStartWithCategories"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.Input" />
      <span class="w-16 mx-4">Rating:</span>
      <select-dropdown class="w-24 ml-2 3xl:w-48" :options-width-class="'w-24'" :state="rating"></select-dropdown>
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Labels:</span>
      <select-dropdown
        class="flex-1"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="labels"
        :enable-input-chips-enter-event="false"
        :on-get="getTagTokenStartWith"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.InputChips" />
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Tag field:</span>
      <select-dropdown
        class="flex-1"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="tagFields"
        :enable-input-chips-enter-event="false"
        :on-get="getSettingFrontGalleryStartWithTagFields"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.InputChips" />
    </div>
    <div class="modal-row" v-for="(_, field) in privateState.tagFields" :key="field">
      <span class="w-24 ml-8 mr-4">{{ field }}:</span>
      <select-dropdown
        class="flex-1"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="privateState.tagFields[field]"
        :enable-input-chips-enter-event="false"
        :on-get="privateState.onGets[field]"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.InputChips" />
    </div>
    <div class="modal-row-10">
      <div class="flex ml-auto">
        <ripple-button class="flex mr-2 btn btn-primary" @click="reset"> Reset </ripple-button>
        <ripple-button class="flex btn btn-primary" @click="save"> Save </ripple-button>
      </div>
    </div>
  </modal>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";

import {
  getSettingFrontGalleryStartWithCategories,
  getSettingFrontGalleryStartWithTagFields,
} from "@/api/v1/setting/front/gallery";
import { getTagTokenStartWith } from "@/api/v1/tag/token";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Modal from "@/elements/Modal/Modal.vue";

import { OnGet, SelectDropdownMode, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.d";

import SelectDropdown, { Origin } from "@/elements/Dropdown/SelectDropdown.vue";

import { galleryState } from "@/state/gallery";
import { messageState } from "@/state/message";

import { watchLabels, watchLabelsChipsLength } from "@/utils/label";
import { watchTagFieldsChipsLength, watchTags } from "@/utils/tag";

interface TagFields {
  [key: string]: SelectDropdownState;
}

interface OnGets {
  [key: string]: OnGet;
}

export interface PrivateState {
  json: string;
  tagFields: TagFields;
  onGets: OnGets;
}

export default defineComponent({
  components: { Modal, RippleButton, SelectDropdown },
  setup() {
    const route = useRoute();

    function tokenToOption(token: { id: number; name: string }) {
      return { title: token.name, value: token.id };
    }

    const editor = ref();
    const privateState = reactive<PrivateState>({
      json: undefined,
      tagFields: {},
      onGets: {},
    });

    const category = SelectDropdown.initState() as SelectDropdownState;
    watch(
      () => galleryState.data.attributes.category,
      () => {
        if (category.title !== galleryState.data.attributes.category) {
          category.title = galleryState.data.attributes.category;
        }
      },
    );
    watch(
      () => category.title,
      () => {
        if (category.title && category.title !== galleryState.data.attributes.category) {
          galleryState.data.attributes.category = category.title as string;
        }
      },
    );

    const rating = SelectDropdown.initState() as SelectDropdownState;
    watch(
      () => galleryState.data.attributes.rating,
      () => {
        if (galleryState.data.attributes.rating && galleryState.data.attributes.rating !== rating.title) {
          rating.title = galleryState.data.attributes.rating;
        }
      },
    );
    watch(
      () => rating.title,
      () => {
        if (rating.title && galleryState.data.attributes.rating !== rating.title) {
          galleryState.data.attributes.rating = rating.title;
        }
      },
    );
    rating.options = [
      { title: 0, value: 0 },
      { title: 1, value: 1 },
      { title: 2, value: 2 },
      { title: 3, value: 3 },
      { title: 4, value: 4 },
      { title: 5, value: 5 },
    ];

    const labels = SelectDropdown.initState() as SelectDropdownState;
    watch(...watchLabels(labels, galleryState));
    watch(...watchLabelsChipsLength(labels, galleryState));

    const tagFields = SelectDropdown.initState() as SelectDropdownState;
    watch(...watchTags(privateState, tagFields, galleryState));
    watch(...watchTagFieldsChipsLength(privateState, tagFields, galleryState));

    function saved() {
      editor.value.close();
      messageState.pushWithLink("Gallery tag saved", route.path);
    }

    function save() {
      for (const field in privateState.tagFields) {
        galleryState.data.tags[field] = [];
        for (const chip of privateState.tagFields[field].chips) {
          galleryState.data.tags[field].push(chip.title as string);
        }
      }
      galleryState.save(saved).then(() => {});
    }

    function reset() {
      galleryState.reset();
      messageState.push("Reset");
    }

    function open() {
      editor.value.open();
    }

    function close() {
      editor.value.close();
    }

    return {
      SelectDropdownMode,
      Origin,
      getTagTokenStartWith,
      getSettingFrontGalleryStartWithCategories,
      getSettingFrontGalleryStartWithTagFields,
      editor,
      privateState,
      galleryState,
      category,
      rating,
      labels,
      tagFields,
      save,
      reset,
      open,
      close,
      tokenToOption,
    };
  },
});
</script>
