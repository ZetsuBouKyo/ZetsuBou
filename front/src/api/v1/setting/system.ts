import request from "@/utils/request";
import { Setting } from "@/interface/setting";

export function getSettingSystem() {
    return request({
        url: "/api/v1/setting/system",
        method: "get",
    });
}

export function putSettingSystem(setting: Setting) {
    return request({
        url: "/api/v1/setting/system",
        method: "put",
        data: setting,
    });
}

export function postSettingSystem(setting: Setting) {
    return request({
        url: "/api/v1/setting/system",
        method: "post",
        data: setting,
    });
}

export function postSettingSystemAirflow(setting: Setting) {
    return request({
        url: "/api/v1/setting/system/airflow",
        method: "post",
        data: setting,
    });
}
