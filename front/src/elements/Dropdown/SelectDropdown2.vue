<script setup lang="ts">
import { reactive, ref, watch } from "vue";

import { Origin } from "./Dropdown.interface";
import {
  SelectDropdownGetParam,
  SelectDropdownMode,
  SelectDropdownOnGet,
  SelectDropdownOnGetTip,
  SelectDropdownOnGetToOptions,
  SelectDropdownOnMouseoverOption,
  SelectDropdownOnSelect,
  SelectDropdownOption,
  SelectDropdownScroll,
} from "./SelectDropdown.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Chip from "@/elements/Chip/Chip.vue";
import Dropdown from "@/elements/Dropdown/Dropdown.vue";

const title = defineModel<string | string[] | number>("title", { default: "" });
const selectedValue = defineModel<any>("selectedValue", { default: undefined });
const chips = defineModel<Array<SelectDropdownOption>>("chips", { default: [] });
const options = defineModel<Array<SelectDropdownOption>>("options", { default: [] });

interface Props {
  group: string;
  mode: SelectDropdownMode;
  origin: Origin;
  isAutoCompleteOptionCaseSensitive: boolean;
  isAutoComplete: boolean;
  isInputChipsTitleUnique: boolean;
  widthClass: string;
  optionsWidthClass: string;
  enableInputChipsEnterEvent: boolean;
  onGet: SelectDropdownOnGet<any>;
  onGetToOptions: SelectDropdownOnGetToOptions;
  onSelect: SelectDropdownOnSelect;
  onGetTip: SelectDropdownOnGetTip;
  onMouseoverOption: SelectDropdownOnMouseoverOption;
}

const props = withDefaults(defineProps<Props>(), {
  group: undefined,
  mode: SelectDropdownMode.Button,
  origin: Origin.BottomRight,
  isAutoCompleteOptionCaseSensitive: false,
  isAutoComplete: false,
  isInputChipsTitleUnique: false,
  widthClass: "",
  optionsWidthClass: "w-60",
  enableInputChipsEnterEvent: true,
  onGet: undefined,
  onGetToOptions: undefined,
  onSelect: undefined,
  onGetTip: undefined,
  onMouseoverOption: undefined,
});

interface State {
  scroll: SelectDropdownScroll;
  lastChipInputTitle: any;
  lock: boolean;
  isFocus: boolean;
}

const state = reactive<State>({
  scroll: { isEnd: false },
  lastChipInputTitle: undefined,
  lock: false,
  isFocus: false,
});

const params: SelectDropdownGetParam = {
  page: 1,
  size: 20,
  s: "",
};

const dropdown = ref();

const isCrud = props.onGet !== undefined && props.onGetToOptions !== undefined;

function getChipKey(i: number, chip: SelectDropdownOption) {
  return i.toString() + chip.title ? chip.title.toString() : "" + chip.value ? chip.value.toString() : "";
}

function getData(params: any, isReset: boolean = false) {
  if (!isCrud) {
    return;
  }
  if (isReset) {
    reset();
  }
  if (state.lock) {
    return;
  }
  if (params.s === undefined) {
    params.s = "";
  }
  state.lock = true;
  props.onGet(params).then((response: any) => {
    if (response.status !== 200) {
      state.scroll.isEnd = false;
    }
    const _options = response.data;
    if (_options) {
      if (_options.length === 0) {
        state.scroll.isEnd = true;
      }
      for (let option of _options) {
        const opt = props.onGetToOptions(option);
        opt.raw = option;
        switch (props.mode) {
          case SelectDropdownMode.InputChips:
            let skip = false;
            for (let chip of chips.value) {
              if (chip.title === opt.title && chip.value === opt.value) {
                skip = true;
                break;
              }
            }
            if (skip) {
              continue;
            }
        }

        options.value.push(opt);
      }
    }
    state.lock = false;
  });
}

function reset() {
  if (isCrud) {
    params.page = 1;
    options.value = [];
    state.scroll.isEnd = false;
  }
}

function onOpen() {
  getData(params, true);
}

function select(opt: SelectDropdownOption) {
  switch (props.mode) {
    case SelectDropdownMode.InputChips:
      for (let chip of chips.value) {
        if (props.isInputChipsTitleUnique && chip.title === opt.title) {
          dropdown.value.close();
          return;
        }
        if (chip.title === opt.title && chip.value === opt.value) {
          dropdown.value.close();
          return;
        }
      }
      chips.value.push({ title: opt.title, value: opt.value });
      title.value = undefined;
      selectedValue.value = undefined;
      break;
    case SelectDropdownMode.Button:
    case SelectDropdownMode.Input:
    default:
      title.value = opt.title;
      selectedValue.value = opt.value;
      break;
  }
  if (opt.handler) {
    opt.handler(opt);
  }
  dropdown.value.close();
  if (props.onSelect) {
    props.onSelect(opt);
  }
}

function scrollNext() {
  if (!isCrud || state.scroll.isEnd) {
    return;
  }
  params.page++;
  getData(params);
}

function scroll(event: any) {
  const target = event.target;
  const diff = Math.abs(target.scrollHeight - target.scrollTop - target.clientHeight);
  if (diff <= 1) {
    scrollNext();
  }
}

function focusOpenDropdown() {
  state.isFocus = true;
  dropdown.value.toggle();
}

function mouseoverOption(event: any, opt: SelectDropdownOption) {
  if (props.onMouseoverOption) {
    props.onMouseoverOption(event, opt);
  }
}

function openDropdown() {
  dropdown.value.open();
}

function toggleDropdown() {
  if (state.isFocus) {
    state.isFocus = false;
    return;
  }
  dropdown.value.toggle();
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

function onDeleteChip(title: string | number, value: string | number, index: number) {
  chips.value.splice(index, 1);
}

function updateOptions(title: string, prevTitle: string) {
  if (title !== undefined) {
    state.lastChipInputTitle = prevTitle;
  } else {
    state.lastChipInputTitle = undefined;
  }

  params.s = title as string;
  if (params.s !== undefined) {
    getData(params, true);
  }
}

function updateOptionsByTitle() {
  console.log(title.value);
}

watch(
  () => title.value,
  (title, prevTitle) => {
    switch (props.mode) {
      case SelectDropdownMode.Button:
        return;
      case SelectDropdownMode.Input:
        if (isCrud) {
          updateOptions(title as string, prevTitle as string);
          return;
        }

        if (!props.isAutoComplete || !options.value || options.value.length === 0) {
          return;
        }
        const tmpOptions = JSON.parse(JSON.stringify(options.value));
        options.value = [];
        for (const option of tmpOptions) {
          let optionTitle = option.title;
          let stateTitle = title as string;
          if (!props.isAutoCompleteOptionCaseSensitive) {
            optionTitle = option.title.toLowerCase();
            stateTitle = title.toString().toLowerCase();
          }
          if (optionTitle.startsWith(stateTitle)) {
            options.value.push(option);
          }
        }
      case SelectDropdownMode.InputChips:
        if (!isCrud) {
          return;
        }
        updateOptions(title as string, prevTitle as string);
    }
  },
);

function close() {
  dropdown.value.close();
}

defineExpose({ close });
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
        <div v-if="mode === SelectDropdownMode.Input" class="relative h-full w-full inline-flex items-center">
          <input
            class="w-full modal-input"
            type="search"
            :placeholder="title as string"
            v-model="title"
            @click.stop="toggleDropdown"
            @focus="focusOpenDropdown" />
          <icon-ic-round-expand-more class="absolute text-white right-0 ml-2 mr-3" style="font-size: 1rem" />
        </div>
        <div
          v-if="mode === SelectDropdownMode.InputChips"
          class="flex flex-wrap min-h-14 items-center bg-gray-600 rounded px-2 py-2">
          <chip
            class="flex-initial m-1"
            v-for="(chip, i) in chips"
            :key="getChipKey(i, chip)"
            :index="i"
            :title="chip.title"
            :value="chip.value"
            :on-delete="onDeleteChip" />
          <input
            class="w-2 h-10 p-0 bg-gray-600 text-base 3xl:text-xl border-0 focus:outline-none focus:ring-0 flex-1"
            type="text"
            v-model="title"
            @click.stop="toggleDropdown"
            @focus="focusOpenDropdown"
            @keyup.delete="deleteLastChip"
            @keyup.enter="createChip"
            @keyup="openDropdown" />
        </div>
        <ripple-button
          v-else-if="mode === SelectDropdownMode.Button"
          class="h-full w-full btn-dark inline-flex items-center text-base 3xl:text-xl border-0 py-1 pl-4 pr-3 focus:outline-none rounded"
          @click.stop="toggleDropdown"
          @focus="focusOpenDropdown">
          <span class="truncate">{{ title }}</span>
          <icon-ic-round-expand-more class="ml-auto" style="font-size: 1rem" />
        </ripple-button>
      </template>
      <template v-slot:options>
        <div class="overflow-y-auto scrollbar-gray-900-2 max-h-72 w-full" @scroll="scroll">
          <button
            class="w-full inline-block text-left text-base text-white 3xl:text-xl truncate border-0 px-4 py-3 focus:outline-none hover:bg-gray-600 focus:bg-gray-600 my-1"
            tabindex="0"
            v-for="opt in options"
            :key="opt.value"
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
