import Cookies from "js-cookie";
import jwt_decode from "jwt-decode";
import { reactive } from "vue";

import { BaseState } from "@/interface/state";

import { getToken } from "@/api/v1/token";
import { getUser, putUser, getUserFrontSetting } from "@/api/v1/user/user";

import { messageState } from "@/state/message";

interface UserUpdate {
  name?: string;
  email: string;
  password: string;
  new_password?: string;
}
export interface FrontSetting {
  gallery_preview_size: number;
  video_preview_size: number;
  img_preview_size: number;
  auto_play_time_interval: number;
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
  frontSetting: FrontSetting;
}
export interface UserState extends BaseState<User> {
  signIn: (data: FormData) => any;
  signOut: () => void;
  update: () => any;
}

interface Token {
  sub: string | number;
}

export const userState = reactive<UserState>({
  data: {
    id: undefined,
    name: undefined,
    email: undefined,
    frontSetting: {
      gallery_preview_size: undefined,
      video_preview_size: undefined,
      img_preview_size: undefined,
      auto_play_time_interval: undefined,
    },
  },
  init: () => {
    const token = Cookies.get("token");
    const decoded: Token = jwt_decode(token);
    const id = decoded.sub.toString();
    userState.data.id = id;
    getUser(id).then((response) => {
      const user = response.data;
      if (user) {
        userState.data.name = user.name;
        userState.data.email = user.email;
      }
    });
    getUserFrontSetting(id).then((response) => {
      const setting = response.data;
      if (setting) {
        userState.data.frontSetting.gallery_preview_size = setting.gallery_preview_size;
        userState.data.frontSetting.video_preview_size = setting.gallery_preview_size;
        userState.data.frontSetting.img_preview_size = setting.img_preview_size;
        userState.data.frontSetting.auto_play_time_interval = setting.auto_play_time_interval;
      }
    });
  },
  signIn: async (data: FormData) => {
    return getToken(data).then((response) => {
      const data = response.data;
      if (data) {
        Cookies.remove("token");
        Cookies.set("token", data.access_token);
      }
    });
  },
  signOut: () => {
    Cookies.remove("token");
  },
  update: async () => {
    let password = userState.data.password;
    if (userState.data.oldPassword !== undefined && userState.data.password === undefined) {
      password = userState.data.oldPassword;
    }

    const user: UserUpdate = { email: userState.data.email, password: password };

    if (userState.data.newName !== undefined) {
      user.name = userState.data.newName;
    }
    if (userState.data.newPassword !== undefined) {
      if (userState.data.newPassword !== userState.data.passwordConfirmation) {
        messageState.push("Please enter your password again");
        userState.data.passwordConfirmation = undefined;
        return;
      }
      user.new_password = userState.data.newPassword;
    }

    return putUser(userState.data.id as number, user).then((response) => {
      const data = response.data;
      if (response.status === 200) {
        messageState.push("Saved");
        userState.data.name = data.name;
        userState.data.newName = undefined;
        userState.data.password = undefined;
        userState.data.oldPassword = undefined;
        userState.data.newPassword = undefined;
        userState.data.passwordConfirmation = undefined;
      }
    });
  },
});
