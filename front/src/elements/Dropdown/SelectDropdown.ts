import { reactive } from "vue";

import { SelectDropdownState, SelectDropdownOption } from "./SelectDropdown.interface";

export function initSelectDropdownState(): SelectDropdownState {
  const state = reactive<SelectDropdownState>({
    title: undefined,
    chips: [],
    options: [],
    scroll: {
      isEnd: false,
    },
    isFocus: false,
    clear: () => {
      state.title = undefined;
      state.selectedValue = undefined;
    },
    reset: () => {
      const newState = initSelectDropdownState();
      for (let key in state) {
        state[key] = newState[key];
      }
    },
  });
  return state;
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
