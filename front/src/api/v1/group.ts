import request from "@/utils/request";

export function getGroupTotal() {
  return request({
    url: `/api/v1/total-groups`,
    method: "get",
  });
}

export function getGroup(params: any) {
  return request({
    url: `/api/v1/group`,
    method: "get",
    params: params,
  });
}

export function postGroup(data: any) {
  return request({
    url: `/api/v1/group`,
    method: "post",
    data: data,
  });
}

export function putGroup(data: any) {
  return request({
    url: `/api/v1/group`,
    method: "put",
    data: data,
  });
}

export function deleteGroup(directory_id: string | number) {
  return request({
    url: `/api/v1/group/${directory_id}`,
    method: "delete",
  });
}

export function getGroups(params: any) {
  return request({
    url: `/api/v1/groups`,
    method: "get",
    params: params,
  });
}
