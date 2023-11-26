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
  return runAirflowDag("video-generate-cover", data);
}

export function postSyncStorageMinio(id: number) {
  const data = {
    args: [
      { type: "string", value: "minio" },
      { type: "number", value: id },
    ],
    kwargs: [{ type: "boolean", name: "force", value: true }],
  };
  return runAirflowDag("sync-storage", data);
}

export function postSyncStoragesMinio() {
  const data = { kwargs: [{ type: "boolean", name: "force", value: true }] };
  return runAirflowDag("sync-storages", data);
}

export function getTaskAirflowProgress(id: string) {
  return request({
    url: `/api/v1/task/cmd/progress/${id}`,
    method: "get",
  });
}

export function deleteTaskAirflowProgress(progressID: string) {
  return request({
    url: `/api/v1/task/cmd/progress/${progressID}`,
    method: "delete",
  });
}

export function getTaskAirflowSyncStoragesProgress() {
  return getTaskAirflowProgress("zetsubou.task.progress.sync-storages");
}

export function deleteTaskAirflowSyncStoragesProgress() {
  return deleteTaskAirflowProgress("zetsubou.task.progress.sync-storages");
}
