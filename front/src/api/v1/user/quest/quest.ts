import request from "@/utils/request";

export function getUserQuestTotal(id: string | number) {
    return request({
        url: `/api/v1/user/${id}/total-quests`,
        method: "get",
    });
}

export function getUserQuests(id: string | number, params: any) {
    return request({
        url: `/api/v1/user/${id}/quests`,
        method: "get",
        params: params,
    });
}

export function postUserQuest(userID: string | number, data: any) {
    if (data.user_id === undefined) {
        data.user_id = userID;
    }
    return request({
        url: `/api/v1/user/${userID}/quest`,
        method: "post",
        data: data,
    });
}

export function putUserQuest(userID: string | number, data: any) {
    if (data.user_id === undefined) {
        data.user_id = userID;
    }
    return request({
        url: `/api/v1/user/${userID}/quest`,
        method: "put",
        data: data,
    });
}

export function deleteUserQuest(id: string | number, query_id: string | number) {
    return request({
        url: `/api/v1/user/${id}/quest/${query_id}`,
        method: "delete",
    });
}

export function getUserCurrentQuestProgress(id: string | number) {
    return request({
        url: `/api/v1/user/${id}/current-quest-progress`,
        method: "get",
    });
}
