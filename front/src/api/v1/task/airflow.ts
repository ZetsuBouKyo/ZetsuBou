import request from "@/utils/request";

export function getAirflowDagRun(dagID: string, dagRunID: string) {
  return request({
    url: `/api/v1/task/cmd/dag-run/${dagID}/${dagRunID}`,
    method: "get",
  });
}

function runAirflowDag(dagID: string, data: any) {
  return request({
    url: `/api/v1/task/cmd/run/${dagID}`,
    method: "post",
    data: data,
  });
}

export function postVideoCreateCover(id: string, frame: number) {
  const data = {
    args: [{ type: "string", value: id }],
    kwargs: [
      {
        name: "frame",
        value: frame,
        type: "number",
      },
    ],
  };
  return runAirflowDag("video-create-cover", data);
}

export function postSyncStorageMinio(id: number) {
  const data = {
    args: [
      { type: "string", value: "minio" },
      { type: "number", value: id },
    ],
  };
  return runAirflowDag("sync-storage", data);
}
