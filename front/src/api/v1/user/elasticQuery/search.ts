import request from "@/utils/request";

export function getUserElasticSearchQueryTotal(id: string | number) {
    return request({
        url: `/api/v1/user/${id}/elastic/total-search-queries`,
        method: "get",
    });
}

export function getUserElasticSearchQueries(id: string | number, params: any) {
    return request({
        url: `/api/v1/user/${id}/elastic/search-queries`,
        method: "get",
        params: params,
    });
}

export function getUserElasticSearchQuery(userID: string | number, queryID: string | number) {
    return request({
        url: `/api/v1/user/${userID}/elastic/search-query/${queryID}`,
        method: "get",
    });
}

export function postUserElasticSearchQuery(userID: string | number, data: any) {
    if (data.user_id === undefined) {
        data.user_id = userID;
    }
    return request({
        url: `/api/v1/user/${userID}/elastic/search-query`,
        method: "post",
        data: data,
    });
}

export function putUserElasticSearchQuery(userID: string | number, data: any) {
    if (data.user_id === undefined) {
        data.user_id = userID;
    }
    return request({
        url: `/api/v1/user/${userID}/elastic/search-query`,
        method: "put",
        data: data,
    });
}

export function deleteUserElasticSearchQuery(id: string | number, query_id: string | number) {
    return request({
        url: `/api/v1/user/${id}/elastic/search-query/${query_id}`,
        method: "delete",
    });
}
