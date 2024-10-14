import { reactive } from "vue";

import { DropdownsState, DropdownComponent } from "@/elements/Dropdown/Dropdown.interface";

export const dropdownsState = reactive<DropdownsState>({
    data: {},
    add: (key: string, dropdown: DropdownComponent) => {
        dropdownsState.data[key] = dropdown;
    },
    delete: (key: string) => {
        delete dropdownsState.data[key];
    },
});
