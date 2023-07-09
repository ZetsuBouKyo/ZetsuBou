import { AxiosResponse } from "axios";

import { Tags } from "@/interface/tag";
export interface Source {
  id?: string;
  path?: string;
  tags?: Tags;
  labels?: Array<string>;
  timestamp?: string;
}
export interface SourceDataState<SourceT> {
  data: SourceT;
}
export interface SourceState<SourceT> extends SourceDataState<SourceT> {
  init: (id: string) => Promise<AxiosResponse<SourceT>>;
  reset: () => Promise<AxiosResponse<SourceT>>;
  getTimestamp: () => string;
  save: (successEvent: (response: any) => void) => Promise<AxiosResponse<SourceT>>;
}
