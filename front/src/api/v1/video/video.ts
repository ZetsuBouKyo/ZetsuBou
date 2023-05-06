import request from "@/utils/request";

export function postCover(id: string, frame: number) {
  return request({
    url: `/api/v1/task/cmd/run/video-create-cover`,
    method: "post",
    data: {
      args: [{ type: "string", value: id }],
      kwargs: [
        {
          name: "frame",
          value: frame,
          type: "number",
        },
      ],
    },
  });
}
