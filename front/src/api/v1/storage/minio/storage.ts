import request from "@/utils/request";

export function getStorageMinioCategories() {
  return request({
    url: `/api/v1/storage/minio/storage-categories`,
    method: "get",
  });
}

export function getStorageMinioTotalStorages() {
  return request({
    url: `/api/v1/storage/minio/total-storages`,
    method: "get",
  });
}

export function getStorageMinios(params: any) {
  return request({
    url: `/api/v1/storage/minio/storages`,
    method: "get",
    params: params,
  });
}

export function postStorageMinio(data: any) {
  return request({
    url: `/api/v1/storage/minio/storage`,
    method: "post",
    data: data,
  });
}

export function putStorageMinio(data: any) {
  return request({
    url: `/api/v1/storage/minio/storage`,
    method: "put",
    data: data,
  });
}

export function deleteStorageMinio(directory_id: string | number) {
  return request({
    url: `/api/v1/storage/minio/storage/${directory_id}`,
    method: "delete",
  });
}
