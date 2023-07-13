import request from "@/utils/request";
import { SearchQuery } from "@/interface/search";

export function getAdvancedSearch(query: any) {
  return request({
    url: "/api/v1/gallery/advanced-search",
    method: "get",
    params: query,
  });
}

export function getSearch(query: SearchQuery) {
  return request({
    url: "/api/v1/gallery/search",
    method: "get",
    params: query,
  });
}

export function getRandom(query: SearchQuery) {
  return request({
    url: "/api/v1/gallery/random",
    method: "get",
    params: query,
  });
}
