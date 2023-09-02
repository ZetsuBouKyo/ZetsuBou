import { AxiosResponse } from "axios";

export interface DataState<DataT> {
  data: DataT;
}

export interface BaseState<DataT> extends DataState<DataT> {
  init?: () => void;
}
export interface SourceState<SourceT> extends DataState<SourceT> {
  init: (id: string) => Promise<AxiosResponse<SourceT>>;
  reset: () => Promise<AxiosResponse<SourceT>>;
  getLastUpdated: () => string;
  save: (successEvent: (response: any) => void) => Promise<AxiosResponse<SourceT>>;
}
