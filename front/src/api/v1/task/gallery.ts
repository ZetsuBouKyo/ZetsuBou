import request from "@/utils/request";

export function getTaskGallerySyncAll() {
    return request({
        url: "/api/v1/task/gallery/sync/all",
        method: "get",
    });
}

export function getTaskGallerySyncStatus() {
    return request({
        url: "/api/v1/task/gallery/sync/status",
        method: "get",
    });
}
