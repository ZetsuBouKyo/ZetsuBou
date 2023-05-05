import request from "@/utils/request";

export function setCover(id: string, frame: number) {
  return request({
    url: `/api/v1/video/v/${id}/set-cover?frame=${frame}`,
    method: "get",
  });
}
