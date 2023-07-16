import { BaseState } from "@/interface/state";

export interface RippleButtonStateData {
  lock: boolean;
}

export interface RippleButtonState extends BaseState<RippleButtonStateData> {
  data: {
    lock: boolean;
  };
  lock: () => void;
  unlock: () => void;
}
