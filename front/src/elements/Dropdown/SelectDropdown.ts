import { reactive, watch } from "vue";

import { SelectDropdownState, SelectDropdownOption, SelectDropdownAssignedValue } from "./SelectDropdown.interface";

import { getValue, setValue } from "@/utils/obj";

export function addInputWatch(
  state: SelectDropdownState,
  source: any,
  key: string,
  assigned: SelectDropdownAssignedValue = SelectDropdownAssignedValue.Title,
) {
  watch(
    () => getValue(source, key),
    () => {
      let assignedValue: any;
      let assignedKey: "title" | "selectedValue";
      switch (assigned) {
        case SelectDropdownAssignedValue.Title:
          assignedValue = state.title;
          assignedKey = "title";
          break;
        case SelectDropdownAssignedValue.SelectedValue:
          assignedValue = state.selectedValue;
          assignedKey = "selectedValue";
          break;
      }
      if (assignedValue !== getValue(source, key)) {
        setValue(state, assignedKey, getValue(source, key));
      }
    },
  );
  watch(
    () => String(state.title) + String(state.selectedValue),
    () => {
      let assignedValue: any;
      switch (assigned) {
        case SelectDropdownAssignedValue.Title:
          assignedValue = state.title;
          break;
        case SelectDropdownAssignedValue.SelectedValue:
          assignedValue = state.selectedValue;
          break;
      }
      if (assignedValue !== undefined && assignedValue !== getValue(source, key)) {
        setValue(source, key, assignedValue);
      }
    },
  );
}

export function addInputChipsWatch(state: SelectDropdownState, source: any, key: string) {
  watch(
    () => JSON.stringify(getValue(source, key)),
    () => {
      state.chips = [];
      const sourceChips: Array<string> = getValue(source, key);
      if (sourceChips !== undefined) {
        for (const sourceChip of sourceChips) {
          state.chips.push({ title: sourceChip, value: undefined });
        }
      }
    },
  );
  watch(
    () => state.chips.length,
    () => {
      if (state.chips !== undefined) {
        const value = [];
        for (const chip of state.chips) {
          value.push(chip.title as string);
        }
        setValue(source, key, value);
      }
    },
  );
}

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
    addInputWatch: (source: any, key: string, assigned: SelectDropdownAssignedValue) => {
      addInputWatch(state, source, key, assigned);
    },
    addInputChipsWatch: (source: any, key: string) => {
      addInputChipsWatch(state, source, key);
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
