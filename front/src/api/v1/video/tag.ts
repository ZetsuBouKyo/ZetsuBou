import request from "@/utils/request";

import { Video } from "@/interface/video";

export function getTag(id: string) {
  return request({
    url: `/api/v1/video/v/${id}/tag`,
    method: "get",
  });
}

export function postTag(id: String, video: Video) {
  return request({
    url: `/api/v1/video/v/${id}/tag`,
    method: "post",
    data: video,
  });
}
