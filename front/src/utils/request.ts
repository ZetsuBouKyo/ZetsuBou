import axios from "axios";
import Cookies from "js-cookie";

const request = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 30000,
});

request.interceptors.request.use(
  function (config) {
    const token = Cookies.get("token");
    if (token) {
      config.headers.Authorization = "Bearer " + token;
    }
    if (!config.headers["Content-Type"]) {
      config.headers["Content-Type"] = "application/json";
    }
    return config;
  },
  function (error) {
    // TODO: add err msg
    return Promise.reject(error);
  },
);

// Add a response interceptor
request.interceptors.response.use(
  function (response) {
    // TODO: add msg
    return response;
  },
  function (error) {
    // TODO: add err msg
    return Promise.reject(error);
  },
);

export default request;
