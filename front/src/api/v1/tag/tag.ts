import request from "@/utils/request";
export interface TagAttribute {
  id: number;
  name: string;
  value: string;
}

export interface TagToken {
  id: number;
  name: string;
}
export interface TagInterpretation {
  id: number;
  name: string;
  categories: Array<TagToken>;
  synonyms: Array<TagToken>;
  representative: TagToken;
  attributes: Array<TagAttribute>;
}

export function getTagInterpretation(tagID: number | string) {
  return request({
    url: `/api/v1/tag/${tagID}/interpretation`,
    method: "get",
  });
}

export function postTag(data: any) {
  return request({
    url: `/api/v1/tag`,
    method: "post",
    data: data,
  });
}

export function putTag(data: any) {
  return request({
    url: `/api/v1/tag`,
    method: "put",
    data: data,
  });
}

export function deleteTag(id: string | number) {
  return request({
    url: `/api/v1/tag/${id}`,
    method: "delete",
  });
}

export function searchForTagAttributes(params: any) {
  return request({
    url: `/api/v1/search-for-tag-attributes`,
    method: "get",
    params: params,
  });
}
