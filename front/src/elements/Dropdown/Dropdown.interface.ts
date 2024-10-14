import { BaseState } from "@/interface/state";

export enum Origin {
    BottomLeft,
    BottomRight,
}

export interface DropdownState {
    popout: boolean;
}

export interface OnClick {
    (): void;
}

// TODO: deprecated
export interface OnOpen {
    (): void;
}

export interface DropdownOnOpen {
    (): void;
}

export interface OnClose {
    (): void;
}

export interface DropdownComponent {
    close: () => void;
    group?: string;
}

export interface DropdownComponents {
    [key: string]: DropdownComponent;
}

export interface DropdownsState extends BaseState<DropdownComponents> {
    add: (key: string, component: DropdownComponent) => void;
    delete: (key: string) => void;
}
