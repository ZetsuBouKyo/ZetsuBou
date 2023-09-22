<script setup lang="ts">
import { PropType, reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import {
  SelectDropdownAssignedValue,
  SelectDropdownMode,
  SelectDropdownOnGet,
  SelectDropdownState,
} from "@/elements/Dropdown/SelectDropdown.interface";
import { Source } from "@/interface/source";
import { SourceState } from "@/interface/state";
import { Token } from "@/interface/tag";
import { PrivateState } from "./interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import Modal from "@/elements/Modal/Modal.vue";

import { getTagTokenStartWith } from "@/api/v1/tag/token";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { messageState } from "@/state/message";

import { initRippleButtonState } from "@/elements/Button/RippleButton";
import { watchLabels, watchLabelsChipsLength } from "@/utils/label";
import { watchTagFieldValues, watchTagFieldsChipsLength, watchTags } from "@/utils/tag";

const props = defineProps({
  state: {
    type: Object as PropType<SourceState<Source>>,
    required: true,
  },
  title: {
    type: Object as PropType<string>,
  },
  savedMessage: {
    type: Object as PropType<string>,
  },
  onGetCategoryStartsWith: {
    type: Object as PropType<SelectDropdownOnGet<Token>>,
  },
  onGetTagFieldStartsWith: {
    type: Object as PropType<SelectDropdownOnGet<Token>>,
  },
});
const state = props.state;

const route = useRoute();

function tokenToOption(token: { id: number; name: string }) {
  return { title: token.name, value: token.id };
}

const editor = ref();
const privateState = reactive<PrivateState<Token>>({
  json: undefined,
  tagFields: {},
  onGets: {},
});

const category = initSelectDropdownState() as SelectDropdownState;
category.addInputWatch(state, "data.attributes.category", SelectDropdownAssignedValue.Title);

const rating = initSelectDropdownState() as SelectDropdownState;
rating.addInputWatch(state, "data.attributes.rating", SelectDropdownAssignedValue.Title);
rating.options = [
  { title: 0, value: 0 },
  { title: 1, value: 1 },
  { title: 2, value: 2 },
  { title: 3, value: 3 },
  { title: 4, value: 4 },
  { title: 5, value: 5 },
];

const labels = initSelectDropdownState() as SelectDropdownState;
watch(...watchLabels(labels, state));
watch(...watchLabelsChipsLength(labels, state));

const tagFields = initSelectDropdownState() as SelectDropdownState;
watch(...watchTags(privateState, tagFields, state));
watch(...watchTagFieldsChipsLength(privateState, tagFields, state));
watch(...watchTagFieldValues(privateState, state));

const saveState = initRippleButtonState();
function saved() {
  editor.value.close();
  messageState.pushWithLink(props.savedMessage, route.path);
}
function save() {
  for (const field in privateState.tagFields) {
    state.data.tags[field] = [];
    for (const chip of privateState.tagFields[field].chips) {
      state.data.tags[field].push(chip.title as string);
    }
  }
  saveState.lock();
  state.save(saved).finally(() => {
    saveState.unlock();
  });
}

function reset() {
  state.reset();
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
  <modal ref="editor" :title="title" class="w-full lg:w-1/2 lg:top-12 lg:left-1/4 text-gray-300">
    <div class="modal-row-10">
      <span class="w-32 mr-4">Name:</span>
      <input class="flex-1 modal-input" type="text" :placeholder="state.data.name" v-model="state.data.name" />
    </div>
    <div class="modal-row-10">
      <span class="w-32 mr-4">Raw Name:</span>
      <input class="flex-1 modal-input" type="text" :placeholder="state.data.raw_name" v-model="state.data.raw_name" />
    </div>
    <!-- <div class="modal-row-10">
      <span class="w-32 mr-4">Source:</span>
      <input
        class="flex-1 modal-input"
        type="text"
        :placeholder="state.data.attributes.src"
        v-model="state.data.attributes.src" />
    </div> -->
    <div class="modal-row-10">
      <span class="w-32 mr-4">Category:</span>
      <select-dropdown
        :width-class="'w-48 xl:w-64'"
        :options-width-class="'w-48 xl:w-64'"
        :state="category"
        :on-get="onGetCategoryStartsWith"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.Input" />
      <span class="w-16 mx-4">Rating:</span>
      <select-dropdown
        class="ml-2"
        :width-class="'w-16 xl:w-24  3xl:w-48'"
        :options-width-class="'w-16 xl:w-24  3xl:w-48'"
        :state="rating"></select-dropdown>
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
        :on-get="onGetTagFieldStartsWith"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.InputChips" />
    </div>
    <div class="modal-row" v-for="(_, field) in privateState.tagFields" :key="JSON.stringify(state.data.tags[field])">
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
        <ripple-button class="flex btn btn-primary" :state="saveState" @click="save"> Save </ripple-button>
      </div>
    </div>
  </modal>
</template>
