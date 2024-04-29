import request from "@/utils/request";

export function getUserTotalBookmarks(userID: number) {
    return request({
        url: `/api/v1/user/${userID}/total-bookmarks`,
        method: "get",
    });
}

export function getUserDetailedGalleryBookmarks(userID: number, params: any) {
    return request({
        url: `/api/v1/user/${userID}/bookmarks/gallery/detail`,
        method: "get",
        params: params,
    });
}

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

export function deleteUserBookmarkGallery(userID: number, bookmarkID: number) {
    return request({
        url: `/api/v1/user/${userID}/bookmark/gallery/b/${bookmarkID}`,
        method: "delete",
    });
}
