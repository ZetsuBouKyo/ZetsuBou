import request from "@/utils/request";

export function getGroupTotal() {
    return request({
        url: `/api/v1/total-groups`,
        method: "get",
    });
}

export function deleteGroup(directory_id: string | number) {
    return request({
        url: `/api/v1/group/${directory_id}`,
        method: "delete",
    });
}

export function getGroups(params: any) {
    return request({
        url: `/api/v1/groups`,
        method: "get",
        params: params,
    });
}

export function getGroupWithScope(groupID: number) {
    return request({
        url: `/api/v1/group-with-scopes/${groupID}`,
        method: "get",
    });
}

export function postGroupWithScopeIDs(data: any) {
    return request({
        url: `/api/v1/group-with-scope-ids`,
        method: "post",
        data: data,
    });
}

export function putGroupWithScopeIDs(data: any) {
    return request({
        url: `/api/v1/group-with-scope-ids`,
        method: "put",
        data: data,
    });
}
