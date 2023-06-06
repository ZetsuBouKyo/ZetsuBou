import request from "@/utils/request";

export function deleteGalleryByID(id: String) {
  return request({
    url: `/api/v1/gallery/${id}/delete`,
    method: "delete",
  });
}
