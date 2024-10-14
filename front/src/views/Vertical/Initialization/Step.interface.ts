import { Setting } from "@/interface/setting";

export interface StepState {
    index: number;
    title: string;
    ok: boolean;
    close: boolean;
    next: boolean;
    setting?: Setting;
    steps?: Array<StepState>;
    [key: string]: any;
}

export interface OnFinish {
    (state: StepState): void;
}
