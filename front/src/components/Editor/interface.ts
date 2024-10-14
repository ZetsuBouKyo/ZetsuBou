import { SelectDropdownOnGet, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";

export interface TagFields {
    [key: string]: SelectDropdownState;
}

export interface SelectDropdownOnGets<DataT> {
    [key: string]: SelectDropdownOnGet<DataT>;
}

export interface PrivateState<DataT> {
    json: string;
    tagFields: TagFields;
    onGets: SelectDropdownOnGets<DataT>;
}
