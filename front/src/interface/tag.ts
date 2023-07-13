import { SelectDropdownState, OnGet } from "@/elements/Dropdown/SelectDropdown.d";

export interface Tags {
  [key: string]: Array<string>;
}

interface TagFields {
  [key: string]: SelectDropdownState;
}

interface OnGets {
  [key: string]: OnGet;
}

export interface TagFieldsPrivateState {
  tagFields: TagFields;
  onGets: OnGets;
}
