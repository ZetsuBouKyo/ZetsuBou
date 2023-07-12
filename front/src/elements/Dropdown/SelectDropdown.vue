<template>
  <div class="relative h-full">
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
            v-model="state.title"
            @click.stop="toggleDropdown"
            @focus="focusOpenDropdown" />
          <icon-ic-round-expand-more class="absolute right-0 mx-2" style="font-size: 1rem" />
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

<script lang="ts">
import { AxiosResponse } from "axios";
import { defineComponent, PropType, reactive, ref, watch } from "vue";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Chip from "@/elements/Chip/Chip.vue";
import Dropdown, { Origin } from "@/elements/Dropdown/Dropdown.vue";

import { PaginationGetParam } from "@/elements/Pagination/pagination.d";

export { Origin };

export interface SelectDropdownGetParam extends PaginationGetParam {
  s: string;
  [key: string]: any;
}

export interface SelectDropdownOption {
  title: string | number;
  value?: string | number;
  handler?: (option: SelectDropdownOption) => void;
  raw?: any;
}

export interface SelectDropdownScroll {
  isEnd: boolean;
}

export interface SelectDropdownState {
  title: string | number;
  options: Array<SelectDropdownOption>;
  scroll: SelectDropdownScroll;
  chips?: Array<SelectDropdownOption>;
  selectedValue?: string | number;
  isFocus?: boolean;
}

export interface OnGet {
  (params: SelectDropdownGetParam): Promise<AxiosResponse<Array<any>>>;
}

export interface OnGetToOptions {
  (data: any): SelectDropdownOption;
}

export interface OnSelect {
  (opt: SelectDropdownOption): void;
}

export interface OnGetTip {
  (opt: SelectDropdownOption): string;
}

export interface OnMouseoverOption {
  (event: any, opt: SelectDropdownOption): void;
}

export enum SelectDropdownMode {
  Button,
  Input,
  InputChips,
}

function initState(): SelectDropdownState {
  return reactive<SelectDropdownState>({
    title: undefined,
    chips: [],
    options: [],
    scroll: {
      isEnd: false,
    },
    isFocus: false,
  });
}

export function reset(state: SelectDropdownState) {
  const newState = initState();
  for (let key in state) {
    state[key] = newState[key];
  }
}

export function clear(state: SelectDropdownState) {
  state.title = undefined;
  state.selectedValue = undefined;
}

export function getOptionsFromEnum(e: any): Array<SelectDropdownOption> {
  const keys = Object.keys(e);
  const options = [];
  for (let key of keys) {
    options.push({ title: e[key], value: e[key] });
  }
  return options;
}

export default defineComponent({
  components: { Chip, Dropdown, RippleButton },
  initState,
  props: {
    state: {
      type: Object as PropType<SelectDropdownState>,
      default: initState(),
    },
    group: {
      type: Object as PropType<string>,
      default: undefined,
    },
    mode: {
      type: Object as PropType<SelectDropdownMode>,
      default: SelectDropdownMode.Button,
    },
    options: {
      type: Object as PropType<Array<SelectDropdownOption>>,
      default: [],
    },
    origin: {
      type: Object as PropType<Origin>,
      default: Origin.BottomRight,
    },
    isAutoCompleteOptionCaseSensitive: {
      type: Object as PropType<boolean>,
      default: false,
    },
    isAutoComplete: {
      type: Object as PropType<boolean>,
      default: false,
    },
    isInputChipsTitleUnique: {
      type: Object as PropType<boolean>,
      default: false,
    },
    optionsWidthClass: {
      type: Object as PropType<string>,
      default: "w-60",
    },
    enableInputChipsEnterEvent: {
      type: Object as PropType<boolean>,
      default: true,
    },
    onGet: {
      type: Object as PropType<OnGet>,
      default: undefined,
    },
    onGetToOptions: {
      type: Object as PropType<OnGetToOptions>,
      default: undefined,
    },
    onSelect: {
      type: Object as PropType<OnSelect>,
      default: undefined,
    },
    onGetTip: {
      type: Object as PropType<OnGetTip>,
      default: undefined,
    },
    onMouseoverOption: {
      type: Object as PropType<OnMouseoverOption>,
      default: undefined,
    },
  },
  setup(props) {
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
      if (target.scrollHeight - target.scrollTop === target.clientHeight) {
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

    return {
      ...props,
      dropdown,
      SelectDropdownMode,
      onOpen,
      select,
      scroll,
      close,
      getChipKey,
      focusOpenDropdown,
      mouseoverOption,
      toggleDropdown,
      openDropdown,
      deleteLastChip,
      createChip,
      onDeleteChip,
    };
  },
});
</script>
