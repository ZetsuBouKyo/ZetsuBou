import request from "@/utils/request";

export function getQueryExample() {
    return request({
        url: "/api/v1/elasticsearch/query-examples",
        method: "get",
    });
}

export function getGalleryFieldNames() {
    return request({
        url: "/api/v1/elasticsearch/gallery/field-names",
        method: "get",
    });
}

export function getVideoFieldNames() {
    return request({
        url: "/api/v1/elasticsearch/video/field-names",
        method: "get",
    });
}
