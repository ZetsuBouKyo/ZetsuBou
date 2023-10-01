import { AxiosResponse } from "axios";

import {
  SelectDropdownOnGetTip,
  SelectDropdownOnGetToOptions,
  SelectDropdownOnMouseoverOption,
} from "@/elements/Dropdown/SelectDropdown.interface";
import { Pagination, PaginationGetParam } from "@/elements/Pagination/pagination.interface";

export interface Header {
  title: string;
  key: string;
  handler?: (value: any) => string | number;
}

export interface Row {
  id?: number;
  [key: string]: any;
}

export interface CrudGetParam extends PaginationGetParam {
  [key: string]: any;
}

export interface Sheet {
  headers: Array<Header>;
  rows: Array<Row>;
}

export enum EditorTypeEnum {
  Create = "create",
  Update = "update",
}

export interface CrudTableState<Row> {
  sheet: Sheet;
  pagination: Pagination;
  row: Row;
  cache: Row;
  editor: {
    type?: EditorTypeEnum;
    handler: () => void;
    title: string;
  };
  [key: string]: any;
}

export interface Editor {
  popout: boolean;
}

export interface OnSearch {
  (params: CrudGetParam): Promise<AxiosResponse<Array<Row>>>;
}

export interface SearchOption {
  title: string;
  onSearch: OnSearch;
  onSearchToOptions: SelectDropdownOnGetToOptions;
  onSearchGetTip?: SelectDropdownOnGetTip;
  onSearchMouseoverOption?: SelectDropdownOnMouseoverOption;
}

export interface Search {
  [key: string]: SearchOption;
}

export interface OnCrudCreate {
  (row: Row): Promise<AxiosResponse<Row>>;
}

export interface OnCrudGet {
  (params: CrudGetParam): Promise<AxiosResponse<Array<Row>>>;
}

export interface OnCrudGetTotal {
  (): Promise<AxiosResponse<number>>;
}

export interface OnCrudUpdate {
  (row: Row): Promise<AxiosResponse<any>>;
}

export interface OnCrudDelete {
  (id: number): Promise<AxiosResponse<Array<any>>>;
}

export interface OnOpenEditor {
  (): void;
}

export interface OnCloseEditor {
  (): void;
}
