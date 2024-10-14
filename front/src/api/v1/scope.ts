import request from "@/utils/request";

export function getScopesStartsWith(params: any) {
    return request({
        url: `/api/v1/scopes-startswith`,
        method: "get",
        params: params,
    });
}
