import request from "@/utils/request";

export function getTaskStandaloneSyncNewGalleries() {
  return request({
    url: "/api/v1/task/standalone/gallery/sync-new-galleries",
    method: "get",
  });
}

export function getTaskStandaloneGalleryOpen(id: String) {
  return request({
    url: `/api/v1/task/standalone/gallery/g/${id}/open`,
    method: "get",
  });
}
