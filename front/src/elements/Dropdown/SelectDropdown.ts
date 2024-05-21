import { reactive, Ref, watch } from "vue";

import {
  SelectDropdownAssignedValue,
  SelectDropdownOption,
  SelectDropdownRequest,
  SelectDropdownDataToOptions,
  SelectDropdownState,
  SelectDropdownToOption,
} from "./SelectDropdown.interface";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";

import { getValue, setValue } from "@/utils/obj";

function updateInputWatch(
  state: SelectDropdownState,
  source: any,
  key: string,
  assigned: SelectDropdownAssignedValue = SelectDropdownAssignedValue.Title,
) {
  if (source === undefined) {
    return;
  }
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
}

export function addInputWatch(
  state: SelectDropdownState,
  source: any,
  key: string,
  assigned: SelectDropdownAssignedValue = SelectDropdownAssignedValue.Title,
) {
  updateInputWatch(state, source, key, assigned);
  watch(
    () => getValue(source, key),
    () => {
      updateInputWatch(state, source, key, assigned);
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

function updateInputChipsWatchByValue(state: SelectDropdownState, source: any, key: string) {
  state.chips = [];
  const sourceChips: Array<string> = getValue(source, key);
  if (sourceChips !== undefined) {
    for (const sourceChip of sourceChips) {
      state.chips.push({ title: sourceChip, value: undefined });
    }
  }
}

function updateInputChipsWatchByLength(state: SelectDropdownState, source: any, key: string) {
  if (state.chips !== undefined) {
    const value = [];
    for (const chip of state.chips) {
      value.push(chip.title as string);
    }
    setValue(source, key, value);
  }
}

export function addInputChipsWatch(state: SelectDropdownState, source: any, key: string) {
  updateInputChipsWatchByValue(state, source, key);
  watch(
    () => JSON.stringify(getValue(source, key)),
    () => {
      updateInputChipsWatchByValue(state, source, key);
    },
  );
  updateInputChipsWatchByLength(state, source, key);
  watch(
    () => state.chips.length,
    () => {
      updateInputChipsWatchByLength(state, source, key);
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

export function convertArrayDataToOptions<T>(
  convertToOption: SelectDropdownToOption<T>,
  data: Array<T>,
  options: Ref<Array<SelectDropdownOption>>,
) {
  for (const d of data) {
    const opt = convertToOption(d);
    opt.raw = d;
    options.value.push(opt);
  }
}

export function convertArrayDataToInputChipsOptions<T>(
  convertToOption: SelectDropdownToOption<T>,
  data: Array<T>,
  options: Ref<Array<SelectDropdownOption>>,
  chips: Ref<Array<SelectDropdownOption>>,
) {
  for (const d of data) {
    const opt = convertToOption(d);
    opt.raw = d;

    let skip = false;
    for (const chip of chips.value) {
      if (chip.title === opt.title && chip.value === opt.value) {
        skip = true;
        break;
      }
    }
    if (skip) {
      continue;
    }

    options.value.push(opt);
  }
}

export function getOptions<DataT, ParamT extends PaginationGetParam>(
  request: SelectDropdownRequest<DataT, ParamT>,
  convertDataToOptions: SelectDropdownDataToOptions<DataT>,
  params: Ref<ParamT>,
  options: Ref<Array<SelectDropdownOption>>,
  lock: Ref<boolean>,
  scrollEnd: Ref<boolean>,
) {
  if (lock.value) {
    return;
  }
  lock.value = true;
  request(params.value).then((response: any) => {
    if (response.status !== 200) {
      scrollEnd.value = false;
    }
    const _options = response.data;
    if (_options) {
      if (_options.length === 0) {
        scrollEnd.value = true;
      }
      convertDataToOptions(_options, options);
    }
    lock.value = false;
  });
}

export function getFirstOptions<DataT, ParamT extends PaginationGetParam>(
  request: SelectDropdownRequest<DataT, ParamT>,
  convertDataToOptions: SelectDropdownDataToOptions<DataT>,
  params: Ref<ParamT>,
  options: Ref<Array<SelectDropdownOption>>,
  lock: Ref<boolean>,
  scrollEnd: Ref<boolean>,
) {
  params.value.page = 1;
  options.value = [];
  scrollEnd.value = false;

  getOptions(request, convertDataToOptions, params, options, lock, scrollEnd);
}

export function scroll<DataT, ParamT extends PaginationGetParam>(
  event: UIEvent,
  request: SelectDropdownRequest<DataT, ParamT>,
  convertDataToOptions: SelectDropdownDataToOptions<DataT>,
  params: Ref<ParamT>,
  options: Ref<Array<SelectDropdownOption>>,
  lock: Ref<boolean>,
  scrollEnd: Ref<boolean>,
) {
  const target = event.target as HTMLElement;
  const diff = Math.abs(target.scrollHeight - target.scrollTop - target.clientHeight);
  if (diff <= 1) {
    if (scrollEnd.value) {
      return;
    }
    params.value.page++;
    getOptions<DataT, ParamT>(request, convertDataToOptions, params, options, lock, scrollEnd);
  }
}
