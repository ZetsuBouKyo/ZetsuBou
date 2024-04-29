import request from "@/utils/request";

export function getSettingFrontVideoInterpretation() {
    return request({
        url: `/api/v1/setting/front/video/interpretation`,
        method: "get",
    });
}

export function putSettingFrontVideo(data: any) {
    return request({
        url: `/api/v1/setting/front/video`,
        method: "put",
        data: data,
    });
}

export function getSettingFrontVideoStartsWithCategories(params: any) {
    return request({
        url: `/api/v1/setting/front/video/category-startswith`,
        method: "get",
        params: params,
    });
}

export function getSettingFrontVideoStartsWithTagFields(params: any) {
    return request({
        url: `/api/v1/setting/front/video/tag-field-startswith`,
        method: "get",
        params: params,
    });
}
