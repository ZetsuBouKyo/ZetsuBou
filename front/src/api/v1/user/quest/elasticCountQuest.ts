import request from "@/utils/request";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";

export function getUserElasticCountQuestTotal(id: string | number) {
  return request({
    url: `/api/v1/user/${id}/total-elastic-count-quests`,
    method: "get",
  });
}

export function getUserElasticCountQuests(id: string | number, params: PaginationGetParam) {
  return request({
    url: `/api/v1/user/${id}/elastic-count-quests`,
    method: "get",
    params: params,
  });
}

export function getUserElasticCountQuest(userID: string | number, questID: string | number) {
  return request({
    url: `/api/v1/user/${userID}/elastic-count-quest/${questID}`,
    method: "get",
  });
}

export function postUserElasticCountQuest(id: string | number, data: any) {
  return request({
    url: `/api/v1/user/${id}/elastic-count-quest`,
    method: "post",
    data: data,
  });
}

export function putUserElasticCountQuest(id: string | number, data: any) {
  return request({
    url: `/api/v1/user/${id}/elastic-count-quest`,
    method: "put",
    data: data,
  });
}

export function deleteUserElasticCountQuest(id: string | number, query_id: string | number) {
  return request({
    url: `/api/v1/user/${id}/elastic-count-quest/${query_id}`,
    method: "delete",
  });
}
