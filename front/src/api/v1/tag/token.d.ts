import { SelectDropdownGetParam } from "@/elements/Dropdown/SelectDropdown.vue";

export interface GetTagTokenStartWithParam extends SelectDropdownGetParam {
  category?: string;
  category_id?: number;
}
