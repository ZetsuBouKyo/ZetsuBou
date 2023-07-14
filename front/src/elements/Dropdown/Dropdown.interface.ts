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

export interface OnOpen {
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
  [key: number]: DropdownComponent;
}

export interface DropdownsState extends BaseState<DropdownComponents> {
  add: (key: number, component: DropdownComponent) => void;
  delete: (key: string | number) => void;
}
