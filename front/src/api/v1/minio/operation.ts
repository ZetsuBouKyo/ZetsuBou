import request from "@/utils/request";

export function getMinioList(params: any) {
  return request({
    url: `/api/v1/minio/operation/list`,
    method: "get",
    params: params,
  });
}
