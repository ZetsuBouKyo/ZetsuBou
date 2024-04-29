import { reactive } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import jwt_decode from "jwt-decode";

import { UserState, Token, UserUpdate } from "@/interface/user";

import { getToken } from "@/api/v1/token";
import { getUser, putUser, getUserFrontSettings } from "@/api/v1/user/user";

import { messageState } from "@/state/message";

function updateUser(response: any) {
    const user = response.data;
    if (user) {
        userState.data.name = user.name;
        userState.data.email = user.email;
    }
}

function updateFrontSettings(response: any) {
    const setting = response.data;
    if (setting) {
        userState.data.frontSettings.gallery_image_auto_play_time_interval =
            setting.gallery_image_auto_play_time_interval;
        userState.data.frontSettings.gallery_image_preview_size = setting.gallery_image_preview_size;
        userState.data.frontSettings.gallery_preview_size = setting.gallery_preview_size;
        userState.data.frontSettings.video_preview_size = setting.video_preview_size;
    }
}

export const userState = reactive<UserState>({
    data: {
        id: undefined,
        name: undefined,
        email: undefined,
        frontSettings: {
            gallery_image_auto_play_time_interval: undefined,
            gallery_image_preview_size: undefined,
            gallery_preview_size: undefined,
            video_preview_size: undefined,
        },
    },
    init: async () => {
        const token = Cookies.get("token");
        const decoded: Token = jwt_decode(token);
        const id = decoded.sub.toString();
        userState.data.id = id;
        return Promise.all<any>([getUser(id), getUserFrontSettings(id)]).then(
            axios.spread((response1, response2) => {
                updateUser(response1);
                updateFrontSettings(response2);
            }),
        );
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
