import request from "@/utils/request";

import { UserFrontSettings } from "@/interface/user";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";

export function getUser(id: string | number) {
    return request({
        url: `/api/v1/user/${id}`,
        method: "get",
    });
}

export function postUserWithGroups(user: any) {
    return request({
        url: `/api/v1/user`,
        method: "post",
        data: user,
    });
}

export function putUser(id: string | number, user: any) {
    return request({
        url: `/api/v1/user/${id}`,
        method: "put",
        data: user,
    });
}

export function putUserWithGroups(id: string | number, user: any) {
    return request({
        url: `/api/v1/user/${id}/with-groups`,
        method: "put",
        data: user,
    });
}

export function deleteUser(id: number) {
    return request({
        url: `/api/v1/user/${id}`,
        method: "delete",
    });
}

export function getUserFrontSettings(id: string | number) {
    return request({
        url: `/api/v1/user/${id}/front-settings`,
        method: "get",
    });
}

export function putUserFrontSettings(id: string | number, settings: UserFrontSettings) {
    return request({
        url: `/api/v1/user/${id}/front-settings`,
        method: "put",
        data: settings,
    });
}

export function getUsers(params: PaginationGetParam) {
    return request({
        url: `/api/v1/users/with-groups`,
        method: "get",
        params: params,
    });
}

export function getUsersTotal() {
    return request({
        url: `/api/v1/total-users`,
        method: "get",
    });
}
