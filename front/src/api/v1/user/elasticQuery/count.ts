import request from "@/utils/request";

export function getUserElasticCountQueryTotal(id: string | number) {
  return request({
    url: `/api/v1/user/${id}/elastic/total-count-queries`,
    method: "get",
  });
}

export function getUserElasticCountQueries(id: string | number, params: any) {
  return request({
    url: `/api/v1/user/${id}/elastic/count-queries`,
    method: "get",
    params: params,
  });
}

export function getUserElasticCountQuery(userID: string | number, queryID: string | number) {
  return request({
    url: `/api/v1/user/${userID}/elastic/count-query/${queryID}`,
    method: "get",
  });
}

export function postUserElasticCountQuery(id: string | number, data: any) {
  return request({
    url: `/api/v1/user/${id}/elastic/count-query`,
    method: "post",
    data: data,
  });
}

export function putUserElasticCountQuery(id: string | number, data: any) {
  return request({
    url: `/api/v1/user/${id}/elastic/count-query`,
    method: "put",
    data: data,
  });
}

export function deleteUserElasticCountQuery(id: string | number, queryID: string | number) {
  return request({
    url: `/api/v1/user/${id}/elastic/count-query/${queryID}`,
    method: "delete",
  });
}
