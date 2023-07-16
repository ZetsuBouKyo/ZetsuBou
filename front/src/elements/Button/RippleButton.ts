import { reactive } from "vue";

import { RippleButtonState } from "./RippleButton.interface";

export function initRippleButtonState(): RippleButtonState {
  const state = reactive<RippleButtonState>({
    data: { lock: false },
    lock: () => {
      state.data.lock = true;
    },
    unlock: () => {
      state.data.lock = false;
    },
  });
  return state;
}
