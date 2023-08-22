<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import {
  OnGet,
  SelectDropdownAssignedValue,
  SelectDropdownMode,
  SelectDropdownState,
} from "@/elements/Dropdown/SelectDropdown.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import Modal from "@/elements/Modal/Modal.vue";

import {
  getSettingFrontVideoStartWithCategories,
  getSettingFrontVideoStartWithTagFields,
} from "@/api/v1/setting/front/video";
import { getTagTokenStartWith } from "@/api/v1/tag/token";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { messageState } from "@/state/message";
import { videoState } from "@/state/video";

import { watchLabels, watchLabelsChipsLength } from "@/utils/label";
import { watchTagFieldValues, watchTagFieldsChipsLength, watchTags } from "@/utils/tag";

interface TagFields {
  [key: string]: SelectDropdownState;
}

interface OnGets {
  [key: string]: OnGet;
}

interface PrivateState {
  json: string;
  tagFields: TagFields;
  onGets: OnGets;
}

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

const category = initSelectDropdownState() as SelectDropdownState;
category.addInputWatch(videoState, "data.attributes.category", SelectDropdownAssignedValue.Title);

const rating = initSelectDropdownState() as SelectDropdownState;
rating.addInputWatch(videoState, "data.attributes.rating", SelectDropdownAssignedValue.Title);
rating.options = [
  { title: 0, value: 0 },
  { title: 1, value: 1 },
  { title: 2, value: 2 },
  { title: 3, value: 3 },
  { title: 4, value: 4 },
  { title: 5, value: 5 },
];

const labels = initSelectDropdownState() as SelectDropdownState;
watch(...watchLabels(labels, videoState));
watch(...watchLabelsChipsLength(labels, videoState));

const tagFields = initSelectDropdownState() as SelectDropdownState;
watch(...watchTags(privateState, tagFields, videoState));
watch(...watchTagFieldsChipsLength(privateState, tagFields, videoState));
watch(...watchTagFieldValues(privateState, videoState));

function saved() {
  editor.value.close();
  messageState.pushWithLink("Video tag saved", route.path);
}

function save() {
  for (const field in privateState.tagFields) {
    videoState.data.tags[field] = [];
    for (const chip of privateState.tagFields[field].chips) {
      videoState.data.tags[field].push(chip.title as string);
    }
  }
  videoState.save(saved).then(() => {});
}

function reset() {
  videoState.reset();
  messageState.push("Reset");
}

function open() {
  window.scrollTo(0, 0);
  editor.value.open();
}

function close() {
  editor.value.close();
}
defineExpose({ open, close, reset });
</script>

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
    <div
      class="modal-row"
      v-for="(_, field) in privateState.tagFields"
      :key="JSON.stringify(videoState.data.tags[field])">
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
