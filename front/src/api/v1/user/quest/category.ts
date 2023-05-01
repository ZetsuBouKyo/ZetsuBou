import request from "@/utils/request";

export function getUserQuestCategories(params: any) {
  return request({
    url: "/api/v1/user/quest/categories",
    method: "get",
    params: params,
  });
}

export function getUserQuestCategory(categoryID: string | number) {
  return request({
    url: `/api/v1/user/quest/category/${categoryID}`,
    method: "get",
  });
}
