import request from "@/utils/request";

import { GetTagTokenStartWithParam } from "@/api/v1/tag/token.d";

export function getTagTokenTotal() {
  return request({
    url: `/api/v1/tag/total-tokens`,
    method: "get",
  });
}

export function getTagTokens(params: any) {
  return request({
    url: `/api/v1/tag/tokens`,
    method: "get",
    params: params,
  });
}

export function getTagTokenStartWith(params: GetTagTokenStartWithParam) {
  return request({
    url: `/api/v1/tag/token-startswith`,
    method: "get",
    params: params,
  });
}

export function postTagToken(data: any) {
  return request({
    url: `/api/v1/tag/token`,
    method: "post",
    data: data,
  });
}

export function putTagToken(data: any) {
  return request({
    url: `/api/v1/tag/token`,
    method: "put",
    data: data,
  });
}

export function deleteTagToken(id: string | number) {
  return request({
    url: `/api/v1/tag/token/${id}`,
    method: "delete",
  });
}
