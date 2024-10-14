import request from "@/utils/request";

import { Gallery } from "@/interface/gallery";

export function getGalleryTag(id: String): Promise<any> {
    return request({
        url: `/api/v1/gallery/${id}/tag`,
        method: "get",
    });
}

export function postGalleryTag(id: String, gallery: Gallery) {
    return request({
        url: `/api/v1/gallery/${id}/tag`,
        method: "post",
        data: gallery,
    });
}
