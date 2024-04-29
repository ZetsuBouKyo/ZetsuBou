import { SelectDropdownGetParam } from "@/elements/Dropdown/SelectDropdown.interface";

export interface GetTagTokenStartsWithParam extends SelectDropdownGetParam {
    category?: string;
    category_id?: number;
}
