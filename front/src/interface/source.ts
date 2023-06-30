import { AxiosResponse } from "axios";

export interface SourceDataState<Source> {
  data: Source;
}
export interface SourceState<Source> extends SourceDataState<Source> {
  init: (id: string) => Promise<AxiosResponse<Source>>;
  reset: () => Promise<AxiosResponse<Source>>;
  getTimestamp: () => string;
  save: () => Promise<AxiosResponse<Source>>;
}
