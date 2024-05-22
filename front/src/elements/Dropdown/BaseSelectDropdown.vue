<script setup lang="ts">
import { ref } from "vue";

import { Origin, DropdownOnOpen } from "./Dropdown.interface";
import {
  SelectDropdownOnGetTip,
  SelectDropdownOnMouseoverOption,
  SelectDropdownOnSelect,
  SelectDropdownOnScroll,
  SelectDropdownOption,
} from "./SelectDropdown.interface";

import Dropdown from "@/elements/Dropdown/Dropdown.vue";

const options = defineModel<Array<SelectDropdownOption>>("options", { default: [] });
const scrollEnd = defineModel<boolean>("scrollEnd", { default: false });

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
  onScroll: undefined,
  onSelect: undefined,
  onGetTip: undefined,
  onMouseoverOption: undefined,
});

function scroll(event: any) {
  if (props.onScroll) {
    props.onScroll(event);
  }
}

function mouseoverOption(event: any, opt: SelectDropdownOption) {
  if (props.onMouseoverOption) {
    props.onMouseoverOption(event, opt);
  }
}

const dropdown = ref();

function select(opt: SelectDropdownOption) {
  if (opt.handler) {
    opt.handler(opt);
  }
  dropdown.value.close();
  if (props.onSelect) {
    props.onSelect(opt);
  }
}

function open() {
  dropdown.value.open();
}

function close() {
  dropdown.value.close();
}

function toggle() {
  dropdown.value.toggle();
}

function reset() {
  while (options?.value.length) {
    options.value.pop();
  }
  scrollEnd.value = false;
}

defineExpose({ open, close, toggle, reset });
</script>

<template>
  <div class="relative h-full" :class="widthClass">
    <dropdown
      ref="dropdown"
      :group="group"
      :origin="origin"
      :select-class="'w-full'"
      :options-width-class="optionsWidthClass"
      :on-open="onOpen"
      :is-expand="false"
      :is-toggle="false">
      <template v-slot:select>
        <slot name="select"></slot>
      </template>
      <template v-slot:options>
        <div class="overflow-y-auto scrollbar-gray-900-2 max-h-72 w-full" @scroll="scroll">
          <button
            class="w-full inline-block text-left text-base text-white 3xl:text-xl truncate border-0 px-4 py-3 focus:outline-none hover:bg-gray-600 focus:bg-gray-600 my-1"
            tabindex="0"
            v-for="opt in options"
            :key="String(opt.title) + String(opt.value)"
            :title="onGetTip ? onGetTip(opt) : undefined"
            @click="select(opt)"
            @mouseover="(event) => mouseoverOption(event, opt)">
            {{ opt.title }}
          </button>
        </div>
      </template>
    </dropdown>
  </div>
</template>
