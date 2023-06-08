import request from "@/utils/request";

export function getUserBookmarkGallery(userID: number, galleryID: string) {
  return request({
    url: `/api/v1/user/${userID}/bookmark/gallery/g/${galleryID}`,
    method: "get",
  });
}

export function postUserBookmarkGallery(userID: number, bookmark: any) {
  return request({
    url: `/api/v1/user/${userID}/bookmark/gallery`,
    method: "post",
    data: bookmark,
  });
}

export function putUserBookmarkGallery(userID: number, bookmark: any) {
  return request({
    url: `/api/v1/user/${userID}/bookmark/gallery`,
    method: "put",
    data: bookmark,
  });
}

export function deleteUserBookmarkGallery(userID: number, bookmarkID: string) {
  return request({
    url: `/api/v1/user/${userID}/bookmark/gallery/b/${bookmarkID}`,
    method: "delete",
  });
}
