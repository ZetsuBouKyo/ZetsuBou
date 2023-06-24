import request from "@/utils/request";

export function checkHostPorts() {
  return request({
    url: "/api/v1/init/check-host-ports",
    method: "get",
  });
}
