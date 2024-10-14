import { reactive } from "vue";

import { getSettingSystem, putSettingSystem } from "@/api/v1/setting/system";

import { SettingSystemState } from "@/state/Setting/system.interface";
import { Setting } from "@/interface/setting";

import { messageState } from "@/state/message";

export const settingSystemState = reactive<SettingSystemState>({
    data: undefined,
    init: () => {
        if (settingSystemState.data !== undefined) {
            return;
        }
        getSettingSystem().then((response) => {
            const data: Setting = response.data;
            settingSystemState.data = data;
        });
    },
    save: () => {
        if (settingSystemState.data === undefined) {
            return;
        }
        putSettingSystem(settingSystemState.data)
            .then((response) => {
                if (response.status === 200) {
                    messageState.push("Saved");
                }
            })
            .catch((error) => {
                messageState.pushError(error);
            });
    },
});
