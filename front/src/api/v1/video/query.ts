import request from "@/utils/request";

export interface SearchQuery {
  analyzer: string;
  query_id: number;
  keywords: string;
  page: number;
  fuzziness: number;
  size: number;
  boolean: "must" | "should";
  seed?: number;
  [key: string]: any;
}

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
