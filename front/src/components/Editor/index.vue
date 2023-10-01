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
import EditorStringArray from "./EditorStringArray.vue";

import { getTagTokenStartWith } from "@/api/v1/tag/token";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { messageState } from "@/state/message";

import { initRippleButtonState } from "@/elements/Button/RippleButton";
import { isLeapYear } from "@/utils/datetime";
import { watchLabels, watchLabelsChipsLength } from "@/utils/label";
import { pad } from "@/utils/number";
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

interface Publication {
  year: string;
  month: string;
  day: string;
  timezone: string;
}
const publication = reactive<Publication>({ year: undefined, month: undefined, day: undefined, timezone: undefined });
function initPublication() {
  if (!state.data.publication_date) {
    return;
  }
  const d = new Date(state.data.publication_date);
  publication.year = pad(d.getFullYear(), 4);
  publication.month = pad(d.getMonth() + 1, 2);
  publication.day = pad(d.getDate(), 2);

  let timezoneOffset = d.getTimezoneOffset();
  let sign = "+";
  if (timezoneOffset > 0) {
    sign = "-";
  } else {
    timezoneOffset = timezoneOffset * -1;
  }
  const timezoneHour = Math.floor(timezoneOffset / 60);
  const timezoneMin = timezoneOffset % 60;

  const tH = pad(timezoneHour, 2);
  const tM = pad(timezoneMin, 2);
  publication.timezone = `${sign}${tH}:${tM}`;
}
initPublication();

function getPublicationDatetime() {
  if (
    (publication.year === undefined || publication.year === "") &&
    (publication.month === undefined || publication.month === "") &&
    (publication.day === undefined || publication.day === "") &&
    (publication.timezone === undefined || publication.timezone === "")
  ) {
    return null;
  }
  const yMessage = "year should be 0000 to 9999";
  const mMessage = "month should be 01 to 12";
  const dMessage = "day should be 01 to 31";
  const dMessage28 = "day should be 01 to 28";
  const dMessage29 = "day should be 01 to 29";
  const tMessage = "timezone should be ±hh:mm";

  const patternYear = /^([0-9][0-9][0-9][0-9])$/;
  const patternMonth = /^(1[0-2]|0[1-9])$/;
  const patternDay = /^(0[1-9]|[1-2][0-9]|3[0-1])$/;
  const patternTimezone = /^(\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$/;

  const year = publication.year.toString();
  const month = publication.month.toString();
  const day = publication.day.toString();
  const timezone = publication.timezone.toString();

  const y = Number(year);
  const m = Number(month);
  const d = Number(day);

  if (isNaN(y) || !year.match(patternYear)) {
    messageState.push(yMessage);
    return undefined;
  }
  if (isNaN(m) || !month.match(patternMonth)) {
    messageState.push(mMessage);
    return undefined;
  }
  if (isNaN(d) || !day.match(patternDay)) {
    messageState.push(dMessage);
    return undefined;
  }
  if (!timezone.match(patternTimezone)) {
    messageState.push(tMessage);
    return undefined;
  }
  if (m === 2) {
    if (isLeapYear(y)) {
      if (d > 29) {
        messageState.push(dMessage29);
        return undefined;
      }
    } else if (d > 28) {
      messageState.push(dMessage28);
      return undefined;
    }
  }

  return `${year}-${month}-${day}T00:00:00.000000${timezone}`;
}

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
  const publicationDate = getPublicationDatetime();
  if (publicationDate === undefined) {
    return;
  }
  state.data.publication_date = publicationDate;

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
    <editor-string-array :title="'Other Names'" :state="state" :state-key="'data.other_names'"></editor-string-array>
    <editor-string-array :title="'Sources'" :state="state" :state-key="'data.src'"></editor-string-array>
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
    <div class="modal-row-10">
      <span class="w-32 mr-4">Publication:</span>
      <input class="modal-input w-20 3xl:w-48" type="text" placeholder="yyyy" v-model="publication.year" />
      <input class="modal-input w-16 3xl:w-48 ml-2" type="text" placeholder="MM" v-model="publication.month" />
      <input class="modal-input w-16 3xl:w-48 ml-2" type="text" placeholder="dd" v-model="publication.day" />
      <input class="modal-input w-28 3xl:w-48 ml-2" type="text" placeholder="±hh:mm" v-model="publication.timezone" />
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
