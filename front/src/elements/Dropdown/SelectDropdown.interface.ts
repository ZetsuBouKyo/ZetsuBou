import { AxiosResponse } from "axios";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";

export enum SelectDropdownAssignedValue {
  Title,
  SelectedValue,
}

export interface SelectDropdownGetParam extends PaginationGetParam {
  s: string;
  [key: string]: any;
}

export interface SelectDropdownOption {
  title: string | number;
  value?: string | number;
  handler?: (option: SelectDropdownOption) => void;
  raw?: any;
}

export interface SelectDropdownScroll {
  isEnd: boolean;
}

export interface SelectDropdownState {
  title: string | number;
  options: Array<SelectDropdownOption>;
  scroll: SelectDropdownScroll;
  chips?: Array<SelectDropdownOption>;
  selectedValue?: string | number;
  isFocus?: boolean;
  clear: () => void;
  reset: () => void;
  addInputWatch: (source: any, key: string, assigned: SelectDropdownAssignedValue) => void;
  addInputChipsWatch: (source: any, key: string) => void;
}

export interface OnGet {
  (params: SelectDropdownGetParam): Promise<AxiosResponse<Array<any>>>;
}

export interface OnGetToOptions {
  (data: any): SelectDropdownOption;
}

export interface OnSelect {
  (opt: SelectDropdownOption): void;
}

export interface OnGetTip {
  (opt: SelectDropdownOption): string;
}

export interface OnMouseoverOption {
  (event: any, opt: SelectDropdownOption): void;
}

export enum SelectDropdownMode {
  Button,
  Input,
  InputChips,
}
