import request from "@/utils/request";
import { SearchQuery } from "@/interface/search";

export function getAdvancedSearch(query: any) {
  return request({
    url: "/api/v1/video/advanced-search",
    method: "get",
    params: query,
  });
}

export function getSearch(query: SearchQuery) {
  return request({
    url: "/api/v1/video/search",
    method: "get",
    params: query,
  });
}

export function getRandom(query: SearchQuery) {
  return request({
    url: "/api/v1/video/random",
    method: "get",
    params: query,
  });
}
