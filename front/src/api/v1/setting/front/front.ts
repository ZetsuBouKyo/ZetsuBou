import request from "@/utils/request";

export function getSettingFrontGeneral() {
  return request({
    url: `/api/v1/setting/front/general`,
    method: "get",
  });
}
