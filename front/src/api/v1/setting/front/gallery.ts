import request from "@/utils/request";

export function getSettingFrontGalleryInterpretation() {
  return request({
    url: `/api/v1/setting/front/gallery/interpretation`,
    method: "get",
  });
}

export function putSettingFrontGallery(data: any) {
  return request({
    url: `/api/v1/setting/front/gallery`,
    method: "put",
    data: data,
  });
}

export function getSettingFrontGalleryStartWithCategories(params: any) {
  return request({
    url: `/api/v1/setting/front/gallery/category-startswith`,
    method: "get",
    params: params,
  });
}

export function getSettingFrontGalleryStartWithTagFields(params: any) {
  return request({
    url: `/api/v1/setting/front/gallery/tag-field-startswith`,
    method: "get",
    params: params,
  });
}
