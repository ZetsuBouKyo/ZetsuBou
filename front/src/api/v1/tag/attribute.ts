import request from "@/utils/request";

export function getTagAttributeTotal() {
    return request({
        url: `/api/v1/tag/total-attributes`,
        method: "get",
    });
}

export function getTagAttributes(params: any) {
    return request({
        url: `/api/v1/tag/attributes`,
        method: "get",
        params: params,
    });
}

export function postTagAttribute(data: any) {
    return request({
        url: `/api/v1/tag/attribute`,
        method: "post",
        data: data,
    });
}

export function putTagAttribute(data: any) {
    return request({
        url: `/api/v1/tag/attribute`,
        method: "put",
        data: data,
    });
}

export function deleteTagAttribute(id: string | number) {
    return request({
        url: `/api/v1/tag/attribute/${id}`,
        method: "delete",
    });
}
