import request from "@/utils/request";

export function getStorageMinioList(params: any) {
    return request({
        url: `/api/v1/storage/minio/list`,
        method: "get",
        params: params,
    });
}
