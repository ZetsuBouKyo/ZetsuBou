import Cookies from "js-cookie";
import jwt_decode from "jwt-decode";

import { reactive } from "vue";

import { getToken } from "@/api/v1/token";
import { getUser, getUserFrontSetting } from "@/api/v1/user/user";

export interface FrontSetting {
  gallery_preview_size: number;
  video_preview_size: number;
  img_preview_size: number;
  auto_play_time_interval: number;
}
export interface User {
  id: string | number;
  name: string;
  email: string;
  frontSetting: FrontSetting;
  init: Function;
  signIn: Function;
  signOut: Function;
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
        Cookies.remove("token", { path: "/", domain: window.location.hostname });
        Cookies.set("token", data.access_token);
      }
    });
  },
  signOut: () => {
    Cookies.remove("token");
  },
});
