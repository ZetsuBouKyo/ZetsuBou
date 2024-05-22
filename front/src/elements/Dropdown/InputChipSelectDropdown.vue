<script setup lang="ts">
import { reactive, ref, Ref, watch } from "vue";

import { DropdownOnOpen, Origin } from "./Dropdown.interface";
import {
  SelectDropdownOnDeleteChip,
  SelectDropdownOnGetTip,
  SelectDropdownOnInput,
  SelectDropdownOnMouseoverOption,
  SelectDropdownOnScroll,
  SelectDropdownOnSelect,
  SelectDropdownOption,
} from "./SelectDropdown.interface";

import BaseSelectDropdown from "./BaseSelectDropdown.vue";
import Chip from "@/elements/Chip/Chip.vue";

interface State {
  lastChipInputTitle: any;
  isFocus: boolean;
}

interface Props {
  group: string;
  origin: Origin;
  isAutoCompleteOptionCaseSensitive: boolean;
  isAutoComplete: boolean;
  isInputChipsTitleUnique: boolean;
  widthClass: string;
  optionsWidthClass: string;
  enableInputChipsEnterEvent: boolean;
  onDeleteChip: SelectDropdownOnDeleteChip;
  onInput: SelectDropdownOnInput;
  onOpen: DropdownOnOpen;
  onScroll: SelectDropdownOnScroll;
  onSelect: SelectDropdownOnSelect;
  onGetTip: SelectDropdownOnGetTip;
  onMouseoverOption: SelectDropdownOnMouseoverOption;
}

const props = withDefaults(defineProps<Props>(), {
  group: undefined,
  origin: Origin.BottomRight,
  isAutoCompleteOptionCaseSensitive: false,
  isAutoComplete: false,
  isInputChipsTitleUnique: false,
  widthClass: "",
  optionsWidthClass: "w-60",
  enableInputChipsEnterEvent: true,
  onDeleteChip: undefined,
  onInput: undefined,
  onOpen: undefined,
  onScroll: undefined,
  onSelect: undefined,
  onGetTip: undefined,
  onMouseoverOption: undefined,
});

const title = defineModel<string | string[] | number | Ref<string | string[] | number>>("title", { default: "" });
const selectedValue = defineModel<any>("selectedValue", { default: undefined });
const chips = defineModel<Array<SelectDropdownOption> | any>("chips", { default: [] });
const defaultOptions = defineModel<Array<SelectDropdownOption> | any>("defaultOptions", { default: [] });
let options = defineModel<Array<SelectDropdownOption> | any>("options", { default: [] });
const scrollEnd = defineModel<boolean | any>("scrollEnd", { default: false });

const baseSelectDropdown = ref();

const state = reactive<State>({
  lastChipInputTitle: undefined,
  isFocus: false,
});

function getChipKey(i: number, chip: SelectDropdownOption) {
  let _i: string;
  if (i === undefined) {
    _i = "";
  } else {
    _i = i.toString();
  }

  let _chipTitle: string = "";
  let _chipValue: string = "";
  if (chip !== undefined) {
    if (chip.title !== undefined) {
      _chipTitle = chip.title.toString();
    }
    if (chip.value !== undefined) {
      _chipValue = chip.value.toString();
    }
  }
  return _i + _chipTitle + _chipValue;
}

function select(opt: SelectDropdownOption) {
  for (let chip of chips.value) {
    if (props.isInputChipsTitleUnique && chip.title === opt.title) {
      baseSelectDropdown.value.close();
      return;
    }
    if (chip.title === opt.title && chip.value === opt.value) {
      baseSelectDropdown.value.close();
      return;
    }
  }
  chips.value.push({ title: opt.title, value: opt.value });
  title.value = undefined;
  selectedValue.value = undefined;

  if (props.onSelect) {
    props.onSelect(opt);
  }
}

function focusOpenDropdown() {
  console.log(options.value);
  state.isFocus = true;
  baseSelectDropdown.value.toggle();
}

function openDropdown() {
  baseSelectDropdown.value.open();
}

function toggleDropdown() {
  console.log(options.value);
  if (state.isFocus) {
    state.isFocus = false;
    return;
  }
  baseSelectDropdown.value.toggle();
}

function createChip() {
  if (!props.enableInputChipsEnterEvent || !title.value) {
    return;
  }

  chips.value.push({ title: title.value as string, value: undefined });
  title.value = undefined;
}

function deleteLastChip() {
  if (!state.lastChipInputTitle) {
    chips.value.pop();
  }
  if (title.value !== undefined && title.value.toString().length === 0) {
    title.value = undefined;
  }
}

function deleteChip(title: string | number, value: string | number, index: number) {
  chips.value.splice(index, 1);
  if (props.onDeleteChip !== undefined) {
    props.onDeleteChip(title, value, index);
  }
}

function updateOptions(title: string) {
  props.onInput(title);
}

function updateOptionsWithDefaultOptions(title: string) {
  if (!defaultOptions.value || defaultOptions.value.length === 0) {
    return;
  }

  // We cannot simply use `options.value = []` here.
  while (options?.value.length) {
    options.value.pop();
  }
  for (let option of defaultOptions.value) {
    option = JSON.parse(JSON.stringify(option));
    let optionTitle = option.title as string;
    let stateTitle = title as string;
    if (!props.isAutoCompleteOptionCaseSensitive) {
      optionTitle = optionTitle.toLowerCase();
      stateTitle = title.toString().toLowerCase();
    }
    if (optionTitle.startsWith(stateTitle)) {
      options.value.push(option);
    }
  }
}

watch(
  () => title.value,
  (title, _) => {
    if (!props.isAutoComplete) {
      return;
    }

    if (props.onInput !== undefined) {
      updateOptions(title as string);
    } else {
      updateOptionsWithDefaultOptions(title as string);
    }
    baseSelectDropdown.value.open();
  },
);

function open() {
  baseSelectDropdown.value.open();
}

function close() {
  baseSelectDropdown.value.close();
}

function toggle() {
  baseSelectDropdown.value.toggle();
}

defineExpose({ open, close, toggle });
</script>

<template>
  <base-select-dropdown
    ref="baseSelectDropdown"
    v-model:options="options"
    v-model:scroll-end="scrollEnd"
    :group="group"
    :origin="origin"
    :width-class="widthClass"
    :options-width-class="optionsWidthClass"
    :on-open="onOpen"
    :on-scroll="onScroll"
    :on-select="select"
    :on-get-tip="onGetTip"
    :on-mouseover-option="onMouseoverOption">
    <template v-slot:select>
      <div class="flex flex-wrap min-h-14 items-center bg-gray-600 rounded px-2 py-2">
        <chip
          class="flex-initial m-1"
          v-for="(chip, i) in chips"
          :key="getChipKey(i, chip)"
          :index="i"
          :title="chip.title"
          :value="chip.value"
          :on-delete="deleteChip" />
        <input
          class="w-full h-10 p-0 bg-gray-600 text-base 3xl:text-xl border-0 focus:outline-none focus:ring-0 flex-1"
          type="text"
          v-model="title"
          @click.stop="toggleDropdown"
          @focus="focusOpenDropdown"
          @keyup.delete="deleteLastChip"
          @keyup.enter="createChip"
          @keyup="openDropdown" />
      </div>
    </template>
  </base-select-dropdown>
</template>
