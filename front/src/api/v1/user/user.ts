import request from "@/utils/request";

export function getUser(id: String) {
  return request({
    url: `/api/v1/user/${id}`,
    method: "get",
  });
}

export function getUserFrontSetting(id: String) {
  return request({
    url: `/api/v1/user/${id}/front-setting`,
    method: "get",
  });
}
