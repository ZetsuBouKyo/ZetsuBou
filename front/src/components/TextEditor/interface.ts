import { SourceState } from "@/interface/source";

export interface OnOverwrite {
  (state: SourceState<any>, data: any): void;
}
