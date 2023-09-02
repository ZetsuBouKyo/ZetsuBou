import { SourceState } from "@/interface/state";

export interface OnOverwrite {
  (state: SourceState<any>, data: any): void;
}
