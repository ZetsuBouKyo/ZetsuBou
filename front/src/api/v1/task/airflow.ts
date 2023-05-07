import request from "@/utils/request";

export function getAirflowDagRun(dagID: string, dagRunID: string) {
  return request({
    url: `/api/v1/task/cmd/dag-run/${dagID}/${dagRunID}`,
    method: "get",
  });
}
