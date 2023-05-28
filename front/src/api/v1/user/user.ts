import request from "@/utils/request";

export function getUser(id: string | number) {
  return request({
    url: `/api/v1/user/${id}`,
    method: "get",
  });
}

export function putUser(id: string | number, user: any) {
  return request({
    url: `/api/v1/user/${id}`,
    method: "put",
    data: user,
  });
}

export function getUserFrontSetting(id: string | number) {
  return request({
    url: `/api/v1/user/${id}/front-setting`,
    method: "get",
  });
}
