import request from "@/utils/request";

export function getTaskStandaloneSyncNewGalleries() {
  return request({
    url: "/api/v1/task/standalone/sync-new-galleries",
    method: "get",
  });
}

export function getTaskStandaloneSyncNewProgress() {
  return request({
    url: "/api/v1/task/standalone/sync-new-galleries/progress",
    method: "get",
  });
}

export function deleteTaskStandaloneSyncNewProgress() {
  return request({
    url: "/api/v1/task/standalone/sync-new-galleries/progress",
    method: "delete",
  });
}

export function getTaskStandaloneGalleryOpen(id: String) {
  return request({
    url: `/api/v1/task/standalone/gallery/g/${id}/open`,
    method: "get",
  });
}
