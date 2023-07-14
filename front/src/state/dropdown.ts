import { reactive } from "vue";

import { DropdownsState, DropdownComponent } from "@/elements/Dropdown/Dropdown.interface";

export const dropdownsState = reactive<DropdownsState>({
  data: {},
  init: () => {},
  add: (key: number, dropdown: DropdownComponent) => {
    dropdownsState.data[key] = dropdown;
  },
  delete: (key: number) => {
    delete dropdownsState.data[key];
  },
});
