import { AxiosResponse } from "axios";
import { Ref } from "vue";

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

export interface SelectDropdownOnGet<DataT> {
  (params: SelectDropdownGetParam): Promise<AxiosResponse<Array<DataT>>>;
}

export interface SelectDropdownRequest<DataT, ParamsT> {
  (params: ParamsT): Promise<AxiosResponse<DataT>> | Promise<any>;
}

export interface SelectDropdownToOption<T> {
  (data: T): SelectDropdownOption;
}
export interface SelectDropdownDataToOptions<DataT> {
  (data: DataT, options: Ref<Array<SelectDropdownOption>>): void;
}

export interface SelectDropdownOnGetToOptions {
  (data: any): SelectDropdownOption;
}

export interface SelectDropdownOnGetDataToOption {
  (data: any): SelectDropdownOption;
}

export interface SelectDropdownOnGetOptionHandler {
  (data: any): void;
}

export interface SelectDropdownOnDeleteChip {
  (title: string | number, value?: string | number | any, key?: number): void;
}

export interface SelectDropdownOnInput {
  (s: string): void;
}

export interface SelectDropdownOnScroll {
  (event: WheelEvent): void;
}

export interface SelectDropdownOnSelect {
  (opt: SelectDropdownOption): void;
}

export interface SelectDropdownOnGetTip {
  (opt: SelectDropdownOption): string;
}

export interface SelectDropdownOnMouseoverOption {
  (event: any, opt: SelectDropdownOption): void;
}

export enum SelectDropdownMode {
  Button,
  Input,
  InputChips,
}
