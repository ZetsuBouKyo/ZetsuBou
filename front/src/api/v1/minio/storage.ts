import request from "@/utils/request";

export function getMinioStorageCategories() {
  return request({
    url: `/api/v1/minio/storage-categories`,
    method: "get",
  });
}

export function getMinioTotalStorages() {
  return request({
    url: `/api/v1/minio/total-storages`,
    method: "get",
  });
}

export function getMinioStorages(params: any) {
  return request({
    url: `/api/v1/minio/storages`,
    method: "get",
    params: params,
  });
}

export function postMinioStorage(data: any) {
  return request({
    url: `/api/v1/minio/storage`,
    method: "post",
    data: data,
  });
}

export function putMinioStorage(data: any) {
  return request({
    url: `/api/v1/minio/storage`,
    method: "put",
    data: data,
  });
}

export function deleteMinioStorage(directory_id: string | number) {
  return request({
    url: `/api/v1/minio/storage/${directory_id}`,
    method: "delete",
  });
}
