import request from "@/utils/request";

export function getQueryExample() {
  return request({
    url: "/api/v1/elasticsearch/query-examples",
    method: "get",
  });
}
