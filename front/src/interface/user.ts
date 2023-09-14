import { BaseState } from "@/interface/state";

export interface UserUpdate {
  name?: string;
  email: string;
  password: string;
  new_password?: string;
}

export interface UserFrontSettings {
  gallery_image_auto_play_time_interval: number;
  gallery_image_preview_size: number;
  gallery_preview_size: number;
  video_preview_size: number;
}

export interface User {
  id: string | number;
  name: string;
  newName?: string;
  email: string;
  password?: string;
  oldPassword?: string;
  newPassword?: string;
  passwordConfirmation?: string;
  frontSettings: UserFrontSettings;
}
export interface UserState extends BaseState<User> {
  signIn: (data: FormData) => any;
  signOut: () => void;
  update: () => any;
}

export interface Token {
  sub: string | number;
}
