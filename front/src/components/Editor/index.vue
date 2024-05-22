<script setup lang="ts">
import { PropType, reactive, ref, Ref } from "vue";
import { useRoute } from "vue-router";

import { DropdownOnOpen, Origin } from "@/elements/Dropdown/Dropdown.interface";
import {
  SelectDropdownGetParam,
  SelectDropdownOnDeleteChip,
  SelectDropdownOnGet,
  SelectDropdownOnInput,
  SelectDropdownOnScroll,
  SelectDropdownOnSelect,
  SelectDropdownOption,
  SelectDropdownRequest,
} from "@/elements/Dropdown/SelectDropdown.interface";
import { Source } from "@/interface/source";
import { SourceState } from "@/interface/state";
import { Token } from "@/interface/tag";

import InputChipSelectDropdown from "@/elements/Dropdown/InputChipSelectDropdown.vue";
import InputSelectDropdown from "@/elements/Dropdown/InputSelectDropdown.vue";
import RippleButtonSelectDropdown from "@/elements/Dropdown/RippleButtonSelectDropdown.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";
import Modal from "@/elements/Modal/Modal.vue";
import EditorStringArray from "./EditorStringArray.vue";

import { getTagTokenStartsWith } from "@/api/v1/tag/token";

import { messageState } from "@/state/message";

import { initRippleButtonState } from "@/elements/Button/RippleButton";
import { isLeapYear } from "@/utils/datetime";
import { pad } from "@/utils/number";
import { getFirstOptions, scroll, convertArrayDataToOptions } from "@/elements/Dropdown/SelectDropdown";

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
    type: Object as PropType<SelectDropdownRequest<Array<Token>, SelectDropdownGetParam>>,
  },
  onGetTagFieldStartsWith: {
    type: Object as PropType<SelectDropdownOnGet<Token>>,
  },
});
const state = props.state;

const route = useRoute();

const editor = ref();

function convertToken(data: Array<Token>, options: Ref<Array<SelectDropdownOption>>) {
  convertArrayDataToOptions<Token>(
    (d: Token) => {
      return { title: d.name, value: d.id };
    },
    data,
    options,
  );
}

// Category
const categoryTitle = ref(state.data.attributes.category);
const categorySelectedValue = ref(state.data.attributes.category);
const categoryOptions = ref([]);
const categoryScrollEnd = ref<boolean>(false);

const categoryParams = ref<SelectDropdownGetParam>({ page: 1, size: 20, s: "" });
const categoryLock = ref<boolean>(false);

const convertCategory = convertToken;
function getCategory(params: SelectDropdownGetParam) {
  return props.onGetCategoryStartsWith(params);
}
function inputCategory(s: string) {
  categoryParams.value.s = s;
  openCategory();
}
function openCategory() {
  getFirstOptions<Array<Token>, SelectDropdownGetParam>(
    getCategory,
    convertCategory,
    categoryParams,
    categoryOptions,
    categoryLock,
    categoryScrollEnd,
  );
}
function scrollCategory(event: any) {
  scroll(event, getCategory, convertCategory, categoryParams, categoryOptions, categoryLock, categoryScrollEnd);
}
function selectCategory(opt: SelectDropdownOption) {
  state.data.attributes.category = opt.title as string;
}

// Rating
const ratingTitle = ref(state.data.attributes.rating);
const ratingSelectedValue = ref(state.data.attributes.rating);
const ratingOptions = ref([
  { title: 0, value: 0 },
  { title: 1, value: 1 },
  { title: 2, value: 2 },
  { title: 3, value: 3 },
  { title: 4, value: 4 },
  { title: 5, value: 5 },
]);
function selectRating(opt: SelectDropdownOption) {
  state.data.attributes.rating = opt.value as number;
}

// Publication
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

// Labels
const labelTitle = ref("");
const labelSelectedValue = ref(undefined);
const labelChips = ref([]);
const labelOptions = ref([]);
const labelScrollEnd = ref<boolean>(false);

const labelParams = ref<SelectDropdownGetParam>({ page: 1, size: 20, s: "" });
const labelLock = ref<boolean>(false);

const convertLabel = convertToken;
function getLabel(params: SelectDropdownGetParam) {
  return getTagTokenStartsWith(params);
}
function deleteChipLabel(title: string, value: number, index: number) {
  const i = state.data.labels.indexOf(title);
  if (i === -1) {
    return;
  }
  state.data.labels.splice(i, 1);
}
function inputLabel(s: string) {
  labelParams.value.s = s;
  openLabel();
}
function openLabel() {
  getFirstOptions(getLabel, convertLabel, labelParams, labelOptions, labelLock, labelScrollEnd);
}
function scrollLabel(event: any) {
  scroll(event, getLabel, convertLabel, labelParams, labelOptions, labelLock, labelScrollEnd);
}
function selectLabel(_: SelectDropdownOption) {
  state.data.labels = [];
  for (const chip of labelChips.value) {
    state.data.labels.push(chip.title);
  }
}

function loadLabel() {
  while (labelChips.value.length) {
    labelChips.value.pop();
  }
  for (const label of state.data.labels) {
    labelChips.value.push({ title: label, id: undefined });
  }
}
loadLabel();

// Tag fields
interface TagField {
  title: Ref<string>;
  selectedValue: Ref<number>;
  chips: Ref<Array<SelectDropdownOption>>;
  options: Ref<Array<SelectDropdownOption>>;
  scrollEnd: Ref<boolean>;
  _params: Ref<SelectDropdownGetParam>;
  _lock: Ref<boolean>;
  _convert: (data: Array<Token>, options: Ref<Array<SelectDropdownOption>>) => void;
  _get: (params: SelectDropdownGetParam) => SelectDropdownRequest<Array<Token>, SelectDropdownGetParam>;
  deleteChip: SelectDropdownOnDeleteChip;
  input: SelectDropdownOnInput;
  open: DropdownOnOpen;
  scroll: SelectDropdownOnScroll;
  select: SelectDropdownOnSelect;
}
interface TagFields {
  [key: string]: TagField;
}
const tagFields = reactive<TagFields>({});
const tagFieldTitle = ref("");
const tagFieldSelectedValue = ref(undefined);
const tagFieldChips = ref([]);
const tagFieldOptions = ref([]);
const tagFieldScrollEnd = ref<boolean>(false);

const tagFieldParams = ref<SelectDropdownGetParam>({ page: 1, size: 20, s: "" });
const tagFieldLock = ref<boolean>(false);

const convertTagField = convertToken;
function getTagField(params: SelectDropdownGetParam) {
  return props.onGetTagFieldStartsWith(params);
}
function deleteChipTagField(title: string, value: number, index: number) {
  delete state.data.tags[title];
  delete tagFields[title];
}
function inputTagField(s: string) {
  tagFieldParams.value.s = s;
  openTagField();
}
function openTagField() {
  getFirstOptions(getTagField, convertTagField, tagFieldParams, tagFieldOptions, tagFieldLock, tagFieldScrollEnd);
}
function scrollTagField(event: any) {
  scroll(event, getTagField, convertTagField, tagFieldParams, tagFieldOptions, tagFieldLock, tagFieldScrollEnd);
}

function loadTagFieldValues(tagFieldTitle: string) {
  const _title = ref("");
  const _selectedValue = ref(undefined);
  const _chips = ref([]);
  const _options = ref([]);
  const _scrollEnd = ref(false);
  const _params = ref<SelectDropdownGetParam>({ page: 1, size: 20, s: "" });
  const _lock = ref(false);
  const _get = (params: SelectDropdownGetParam): any => {
    return getTagTokenStartsWith(params);
  };
  const _convert = convertToken;
  const _deleteChip = (title: string, value: number, index: number) => {
    if (!state.data.tags[tagFieldTitle]) {
      return;
    }
    const i = state.data.tags[tagFieldTitle].indexOf(tagFieldTitle);
    if (i === -1) {
      return;
    }
    state.data.tags[tagFieldTitle].splice(i, 1);
  };
  const _open = () => {
    _params.value.category = tagFieldTitle;
    getFirstOptions(_get, _convert, _params, _options, _lock, _scrollEnd);
  };
  const _input = (s: string) => {
    _params.value.s = s;
    _open();
  };
  const _scroll = (event: any) => {
    scroll(event, _get, _convert, _params, _options, _lock, _scrollEnd);
  };
  const _select = (_: SelectDropdownOption) => {
    state.data.tags[tagFieldTitle] = [];
    for (const chip of _chips.value) {
      state.data.tags[tagFieldTitle].push(chip.title);
    }
  };
  tagFields[tagFieldTitle] = {
    title: _title,
    selectedValue: _selectedValue,
    chips: _chips,
    options: _options,
    scrollEnd: _scrollEnd,
    _params: _params,
    _lock: _lock,
    _convert: _convert,
    _get: _get,
    deleteChip: _deleteChip,
    input: _input,
    open: _open,
    scroll: _scroll,
    select: _select,
  };

  if (state.data.tags[tagFieldTitle].length > 0) {
    for (const value of state.data.tags[tagFieldTitle]) {
      _chips.value.push({ title: value, id: undefined });
    }
  }
}

function selectTagField(_: SelectDropdownOption) {
  for (const chip of tagFieldChips.value) {
    const tagFieldTitle = chip.title;
    if (!state.data.tags[tagFieldTitle]) {
      state.data.tags[tagFieldTitle] = [];
    }
    if (!tagFields[tagFieldTitle]) {
      loadTagFieldValues(tagFieldTitle);
    }
  }
}

function loadTagField() {
  for (const tagFieldTitle in state.data.tags) {
    tagFieldChips.value.push({ title: tagFieldTitle, id: undefined });
    loadTagFieldValues(tagFieldTitle);
  }
}
loadTagField();

// Methods
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
      <input-select-dropdown
        v-model:title="categoryTitle"
        v-model:selected-value="categorySelectedValue"
        v-model:options="categoryOptions"
        v-model:scroll-end="categoryScrollEnd"
        :width-class="'w-48 xl:w-64'"
        :options-width-class="'w-48 xl:w-64'"
        :on-input="inputCategory"
        :on-open="openCategory"
        :on-scroll="scrollCategory"
        :on-select="selectCategory" />
      <span class="w-16 mx-4">Rating:</span>
      <ripple-button-select-dropdown
        class="ml-2"
        v-model:title="ratingTitle"
        v-model:selected-value="ratingSelectedValue"
        v-model:options="ratingOptions"
        :on-select="selectRating"
        :width-class="'w-16 xl:w-24  3xl:w-48'"
        :options-width-class="'w-16 xl:w-24  3xl:w-48'" />
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
      <input-chip-select-dropdown
        class="flex-1"
        v-model:title="labelTitle"
        v-model:selected-value="labelSelectedValue"
        v-model:chips="labelChips"
        v-model:options="labelOptions"
        v-model:scroll-end="labelScrollEnd"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :enable-input-chips-enter-event="false"
        :on-delete-chip="deleteChipLabel"
        :on-input="inputLabel"
        :on-open="openLabel"
        :on-scroll="scrollLabel"
        :on-select="selectLabel" />
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Tag field:</span>
      <input-chip-select-dropdown
        class="flex-1"
        v-model:title="tagFieldTitle"
        v-model:selected-value="tagFieldSelectedValue"
        v-model:chips="tagFieldChips"
        v-model:options="tagFieldOptions"
        v-model:scroll-end="tagFieldScrollEnd"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :enable-input-chips-enter-event="false"
        :on-delete-chip="deleteChipTagField"
        :on-input="inputTagField"
        :on-open="openTagField"
        :on-scroll="scrollTagField"
        :on-select="selectTagField" />
    </div>
    <div class="modal-row" v-for="(i, field) in tagFields" :key="String(i)">
      <span class="w-24 ml-8 mr-4">{{ field }}:</span>
      <input-chip-select-dropdown
        class="flex-1"
        v-model:title="tagFields[field].title"
        v-model:selected-value="tagFields[field].selectedValue"
        v-model:chips="tagFields[field].chips"
        v-model:options="tagFields[field].options"
        v-model:scroll-end="tagFields[field].scrollEnd"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :enable-input-chips-enter-event="false"
        :on-delete-chip="tagFields[field].deleteChip"
        :on-input="tagFields[field].input"
        :on-open="tagFields[field].open"
        :on-scroll="tagFields[field].scroll"
        :on-select="tagFields[field].select" />
    </div>
    <div class="modal-row-10">
      <div class="flex ml-auto">
        <ripple-button class="flex mr-2 btn btn-primary" @click="reset"> Reset </ripple-button>
        <ripple-button class="flex btn btn-primary" :state="saveState" @click="save"> Save </ripple-button>
      </div>
    </div>
  </modal>
</template>
