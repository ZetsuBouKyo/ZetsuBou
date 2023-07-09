import Cookies from "js-cookie";
import jwt_decode from "jwt-decode";

import { reactive } from "vue";

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
  init: () => void;
  signIn: (data: FormData) => any;
  signOut: () => void;
  update: () => any;
}

interface Token {
  sub: string | number;
}

export const userState = reactive<User>({
  id: undefined,
  name: undefined,
  email: undefined,
  frontSetting: {
    gallery_preview_size: undefined,
    video_preview_size: undefined,
    img_preview_size: undefined,
    auto_play_time_interval: undefined,
  },
  init: () => {
    const token = Cookies.get("token");
    const decoded: Token = jwt_decode(token);
    const id = decoded.sub.toString();
    userState.id = id;
    getUser(id).then((response) => {
      const user = response.data;
      if (user) {
        userState.name = user.name;
        userState.email = user.email;
      }
    });
    getUserFrontSetting(id).then((response) => {
      const setting = response.data;
      if (setting) {
        userState.frontSetting.gallery_preview_size = setting.gallery_preview_size;
        userState.frontSetting.video_preview_size = setting.gallery_preview_size;
        userState.frontSetting.img_preview_size = setting.img_preview_size;
        userState.frontSetting.auto_play_time_interval = setting.auto_play_time_interval;
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
    let password = userState.password;
    if (userState.oldPassword !== undefined && userState.password === undefined) {
      password = userState.oldPassword;
    }

    const user: UserUpdate = { email: userState.email, password: password };

    if (userState.newName !== undefined) {
      user.name = userState.newName;
    }
    if (userState.newPassword !== undefined) {
      if (userState.newPassword !== userState.passwordConfirmation) {
        messageState.push("Please enter your password again");
        userState.passwordConfirmation = undefined;
        return;
      }
      user.new_password = userState.newPassword;
    }

    return putUser(userState.id as number, user)
      .then((response) => {
        const data = response.data;
        if (response.status === 200) {
          messageState.push("Saved");
          userState.name = data.name;
          userState.newName = undefined;
          userState.password = undefined;
          userState.oldPassword = undefined;
          userState.newPassword = undefined;
          userState.passwordConfirmation = undefined;
        }
      })
      .catch((error) => {
        return messageState.pushError(error);
      });
  },
});
