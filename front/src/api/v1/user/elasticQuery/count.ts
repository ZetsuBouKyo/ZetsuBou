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

export function postUserElasticCountQuery(userID: string | number, data: any) {
  if (data.user_id === undefined) {
    data.user_id = userID;
  }
  return request({
    url: `/api/v1/user/${userID}/elastic/count-query`,
    method: "post",
    data: data,
  });
}

export function putUserElasticCountQuery(userID: string | number, data: any) {
  if (data.user_id === undefined) {
    data.user_id = userID;
  }
  return request({
    url: `/api/v1/user/${userID}/elastic/count-query`,
    method: "put",
    data: data,
  });
}

export function deleteUserElasticCountQuery(userID: string | number, queryID: string | number) {
  return request({
    url: `/api/v1/user/${userID}/elastic/count-query/${queryID}`,
    method: "delete",
  });
}
