<script setup lang="ts">
import { reactive, ref } from "vue";

import { DropdownOnOpen, Origin } from "./Dropdown.interface";
import {
  SelectDropdownOnGetTip,
  SelectDropdownOnMouseoverOption,
  SelectDropdownOnScroll,
  SelectDropdownOnSelect,
  SelectDropdownOption,
} from "./SelectDropdown.interface";

import BaseSelectDropdown from "./BaseSelectDropdown.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";

interface State {
  isFocus: boolean;
}

interface Props {
  group: string;
  origin: Origin;
  widthClass: string;
  optionsWidthClass: string;
  onOpen: DropdownOnOpen;
  onScroll: SelectDropdownOnScroll;
  onSelect: SelectDropdownOnSelect;
  onGetTip: SelectDropdownOnGetTip;
  onMouseoverOption: SelectDropdownOnMouseoverOption;
}

const props = withDefaults(defineProps<Props>(), {
  group: undefined,
  origin: Origin.BottomRight,
  widthClass: "",
  optionsWidthClass: "w-60",
  onOpen: undefined,
  onScroll: undefined,
  onSelect: undefined,
  onGetTip: undefined,
  onMouseoverOption: undefined,
});

const title = defineModel<string | string[] | number>("title", { default: "" });
const selectedValue = defineModel<any>("selectedValue", { default: undefined });
const options = defineModel<Array<SelectDropdownOption>>("options", { default: [] });
const scrollEnd = defineModel<boolean>("scrollEnd", { default: false });

const baseSelectDropdown = ref();

const state = reactive<State>({
  isFocus: false,
});

function select(opt: SelectDropdownOption) {
  title.value = opt.title;
  selectedValue.value = opt.value;

  if (props.onSelect) {
    props.onSelect(opt);
  }
}

function focusOpenDropdown() {
  state.isFocus = true;
  baseSelectDropdown.value.toggle();
}

function toggleDropdown() {
  if (state.isFocus) {
    state.isFocus = false;
    return;
  }
  baseSelectDropdown.value.toggle();
}

function open() {
  baseSelectDropdown.value.open();
}

function close() {
  baseSelectDropdown.value.close();
}

function toggle() {
  baseSelectDropdown.value.toggle();
}

function clear() {
  title.value = "";
  selectedValue.value = undefined;
}

defineExpose({ open, close, toggle, clear });
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
      <ripple-button
        class="h-full w-full btn-dark inline-flex items-center text-base 3xl:text-xl border-0 py-1 pl-4 pr-3 focus:outline-none rounded"
        @click.stop="toggleDropdown"
        @focus="focusOpenDropdown">
        <span class="truncate">{{ title }}</span>
        <icon-ic-round-expand-more class="ml-auto" style="font-size: 1rem" />
      </ripple-button>
    </template>
  </base-select-dropdown>
</template>
