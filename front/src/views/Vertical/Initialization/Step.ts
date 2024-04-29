import { reactive } from "vue";

import { StepState } from "./Step.interface";

export function initStepState(index: number, title: string, close: boolean) {
    return reactive<StepState>({ index: index, title: title, ok: false, close: close, ports: undefined, next: false });
}
