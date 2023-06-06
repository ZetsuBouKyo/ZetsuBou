import request from "@/utils/request";

export function getToken(data: FormData) {
  return request({
    url: "/api/v1/token",
    method: "post",
    headers: {
      "Content-Type": "multipart/form-data",
    },
    data: data,
  });
}
