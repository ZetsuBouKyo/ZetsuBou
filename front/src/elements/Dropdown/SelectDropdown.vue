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
  SelectDropdownState,
} from "./SelectDropdown.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Chip from "@/elements/Chip/Chip.vue";
import Dropdown from "@/elements/Dropdown/Dropdown.vue";

import { initSelectDropdownState } from "./SelectDropdown";

interface Props {
  state: SelectDropdownState;
  group: string;
  mode: SelectDropdownMode;
  default: any;
  options: Array<SelectDropdownOption>;
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
  state: () => initSelectDropdownState() as SelectDropdownState,
  group: undefined,
  mode: SelectDropdownMode.Button,
  default: "",
  options: () => [],
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

const state = props.state;

const privateState = reactive({
  lastChipInputTitle: undefined,
  lock: false,
  options: props.options,
});

if (privateState.options && privateState.options.length > 0) {
  state.options = JSON.parse(JSON.stringify(privateState.options));
}

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

function getData(state: SelectDropdownState, params: any, isReset: boolean = false) {
  if (!isCrud) {
    return;
  }
  if (isReset) {
    reset();
  }
  if (privateState.lock) {
    return;
  }
  privateState.lock = true;
  props.onGet(params).then((response: any) => {
    if (response.status !== 200) {
      state.scroll.isEnd = false;
    }
    const options = response.data;
    if (options) {
      if (options.length === 0) {
        state.scroll.isEnd = true;
      }
      for (let option of options) {
        const opt = props.onGetToOptions(option);
        opt.raw = option;
        switch (props.mode) {
          case SelectDropdownMode.InputChips:
            let skip = false;
            for (let chip of state.chips) {
              if (chip.title === opt.title && chip.value === opt.value) {
                skip = true;
                break;
              }
            }
            if (skip) {
              continue;
            }
        }

        state.options.push(opt);
      }
    }
    privateState.lock = false;
  });
}

function reset() {
  if (isCrud) {
    params.page = 1;
    state.options = [];
    state.scroll.isEnd = false;
  }
}

function onOpen() {
  getData(state, params, true);
}

function select(opt: SelectDropdownOption) {
  switch (props.mode) {
    case SelectDropdownMode.InputChips:
      for (let chip of state.chips) {
        if (props.isInputChipsTitleUnique && chip.title === opt.title) {
          dropdown.value.close();
          return;
        }
        if (chip.title === opt.title && chip.value === opt.value) {
          dropdown.value.close();
          return;
        }
      }
      state.chips.push({ title: opt.title, value: opt.value });
      state.title = undefined;
      state.selectedValue = undefined;
      break;
    case SelectDropdownMode.Button:
    case SelectDropdownMode.Input:
    default:
      state.title = opt.title;
      state.selectedValue = opt.value;
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
  getData(state, params);
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
  if (!props.enableInputChipsEnterEvent || !state.title) {
    return;
  }
  const title = state.title;
  state.chips.push({ title: title, value: undefined });
  state.title = undefined;
}

function deleteLastChip() {
  if (!privateState.lastChipInputTitle) {
    state.chips.pop();
  }
  if (state.title !== undefined && state.title.toString().length === 0) {
    state.title = undefined;
  }
}

function onDeleteChip(title: string | number, value: string | number, index: number) {
  state.chips.splice(index, 1);
}

function updateOptions(title: string, prevTitle: string) {
  if (title !== undefined) {
    privateState.lastChipInputTitle = prevTitle;
  } else {
    privateState.lastChipInputTitle = undefined;
  }

  params.s = state.title as string;
  if (params.s !== undefined) {
    getData(state, params, true);
  }
}

watch(
  () => state.title,
  (title, prevTitle) => {
    switch (props.mode) {
      case SelectDropdownMode.Button:
        return;
      case SelectDropdownMode.Input:
        if (isCrud) {
          updateOptions(title as string, prevTitle as string);
          return;
        }

        if (!props.isAutoComplete || !privateState.options || privateState.options.length === 0) {
          return;
        }
        const tmpOptions = JSON.parse(JSON.stringify(privateState.options));
        state.options = [];
        for (const option of tmpOptions) {
          let optionTitle = option.title;
          let stateTitle = state.title;
          if (!props.isAutoCompleteOptionCaseSensitive) {
            optionTitle = option.title.toLowerCase();
            stateTitle = state.title.toString().toLowerCase();
          }
          if (optionTitle.startsWith(stateTitle)) {
            state.options.push(option);
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
            :placeholder="default"
            v-model="state.title"
            @click.stop="toggleDropdown"
            @focus="focusOpenDropdown" />
          <icon-ic-round-expand-more class="absolute text-white right-0 ml-2 mr-3" style="font-size: 1rem" />
        </div>
        <div
          v-if="mode === SelectDropdownMode.InputChips"
          class="flex flex-wrap min-h-14 items-center bg-gray-600 rounded px-2 py-2">
          <chip
            class="flex-initial m-1"
            v-for="(chip, i) in state.chips"
            :key="getChipKey(i, chip)"
            :index="i"
            :title="chip.title"
            :value="chip.value"
            :on-delete="onDeleteChip" />
          <input
            class="w-2 h-10 p-0 bg-gray-600 text-base 3xl:text-xl border-0 focus:outline-none focus:ring-0 flex-1"
            type="text"
            v-model="state.title"
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
          <span class="truncate">{{ state.title }}</span>
          <icon-ic-round-expand-more class="ml-auto" style="font-size: 1rem" />
        </ripple-button>
      </template>
      <template v-slot:options>
        <div class="overflow-y-auto scrollbar-gray-900-2 max-h-72 w-full" @scroll="scroll">
          <button
            class="w-full inline-block text-left text-base text-white 3xl:text-xl truncate border-0 px-4 py-3 focus:outline-none hover:bg-gray-600 focus:bg-gray-600 my-1"
            tabindex="0"
            v-for="opt in state.options"
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
