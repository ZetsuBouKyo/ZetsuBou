import { SelectDropdownGetParam } from "@/elements/Dropdown/SelectDropdown.interface";

export interface GetTagTokenStartWithParam extends SelectDropdownGetParam {
  category?: string;
  category_id?: number;
}
