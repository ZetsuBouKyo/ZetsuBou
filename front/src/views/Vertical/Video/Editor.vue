<template>
  <modal ref="editor" :title="'Video Editor'" class="w-1/2 top-12 left-1/4 text-gray-300">
    <div class="modal-row-10">
      <span class="w-32 mr-4">Name:</span>
      <input
        class="flex-1 modal-input"
        type="text"
        :placeholder="videoState.data.name"
        v-model="videoState.data.name" />
    </div>
    <div class="modal-row-10">
      <span class="w-32 mr-4">Source:</span>
      <input
        class="flex-1 modal-input"
        type="text"
        :placeholder="videoState.data.attributes.src"
        v-model="videoState.data.attributes.src" />
    </div>
    <div class="modal-row-10">
      <span class="w-32 mr-4">Category:</span>
      <select-dropdown
        class="w-64"
        :options-width-class="'w-64'"
        :state="category"
        :on-get="getSettingFrontVideoStartWithCategories"
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
        :on-get="getSettingFrontVideoStartWithTagFields"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.InputChips" />
    </div>
    <div class="modal-row" v-for="(_, field) in privateState.tagFields" :key="privateState.tagFields[field]">
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

import { getTagTokenStartWith } from "@/api/v1/tag/token";
import {
  getSettingFrontVideoStartWithCategories,
  getSettingFrontVideoStartWithTagFields,
} from "@/api/v1/setting/front/video";

import Modal from "@/elements/Modal/Modal.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";

import SelectDropdown, {
  SelectDropdownState,
  SelectDropdownMode,
  Origin,
  OnGet,
} from "@/elements/Dropdown/SelectDropdown.vue";

import { videoState } from "@/state/video";
import { messageState } from "@/state/message";

import { watchLabelsLength, watchLabelsChipsLength } from "@/utils/label";
import { watchTagsLength, watchTagFieldsChipsLength } from "@/utils/tag";

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
      () => videoState.data.attributes.category,
      () => {
        if (category.title !== videoState.data.attributes.category) {
          category.title = videoState.data.attributes.category;
        }
      },
    );
    watch(
      () => category.title,
      () => {
        if (category.title && category.title !== videoState.data.attributes.category) {
          videoState.data.attributes.category = category.title as string;
        }
      },
    );

    const rating = SelectDropdown.initState() as SelectDropdownState;
    watch(
      () => videoState.data.attributes.rating,
      () => {
        if (videoState.data.attributes.rating && videoState.data.attributes.rating !== rating.title) {
          rating.title = videoState.data.attributes.rating;
        }
      },
    );
    watch(
      () => rating.title,
      () => {
        if (rating.title && videoState.data.attributes.rating !== rating.title) {
          videoState.data.attributes.rating = rating.title as number;
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
    watch(...watchLabelsLength(labels, videoState));
    watch(...watchLabelsChipsLength(labels, videoState));

    const tagFields = SelectDropdown.initState() as SelectDropdownState;
    watch(...watchTagsLength(privateState, tagFields, videoState));
    watch(...watchTagFieldsChipsLength(privateState, tagFields, videoState));

    function save() {
      for (const field in privateState.tagFields) {
        videoState.data.tags[field] = [];
        for (const chip of privateState.tagFields[field].chips) {
          videoState.data.tags[field].push(chip.title as string);
        }
      }
      videoState.save().then(() => {
        editor.value.close();
        messageState.pushWithLink("Video tag saved", route.path);
      });
    }

    function reset() {
      videoState.reset();
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
      getSettingFrontVideoStartWithCategories,
      getSettingFrontVideoStartWithTagFields,
      editor,
      privateState,
      videoState,
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
