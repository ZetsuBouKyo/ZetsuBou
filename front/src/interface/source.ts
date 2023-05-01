import { AxiosResponse } from "axios";

export interface SourceState<Source> {
  data: Source;
  init: (id: string) => Promise<AxiosResponse<Source>>;
  reset: () => Promise<AxiosResponse<Source>>;
  getTimestamp: () => string;
  save: () => Promise<AxiosResponse<Source>>;
}
