import request from "@/utils/request";

export function getImages(id: String) {
  return request({
    url: `/api/v1/gallery/${id}/images`,
    method: "get",
  });
}
