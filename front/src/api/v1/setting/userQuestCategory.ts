import request from "@/utils/request";

export function getSettingUserQuestCategories(params: any) {
  return request({
    url: "/api/v1/setting/user-quest-categories",
    method: "get",
    params: params,
  });
}

export function getSettingUserQuestCategory(categoryID: string | number) {
  return request({
    url: `/api/v1/setting/user-quest-category/${categoryID}`,
    method: "get",
  });
}
