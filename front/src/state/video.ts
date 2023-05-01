import { reactive } from "vue";

import { Video } from "@/interface/video";
import { SourceState } from "@/interface/source";

import { getTag, postTag } from "@/api/v1/video/tag";
import { getDatetime } from "@/utils/datetime";

import { messageState } from "./message";

export const videoState = reactive<SourceState<Video>>({
  data: {
    id: undefined,
    name: undefined,
    other_names: [],
    path: undefined,
    attributes: {
      category: undefined,
      rating: undefined,
      height: undefined,
      width: undefined,
      uploader: undefined,
      duration: undefined,
      fps: undefined,
      frames: undefined,
      md5: undefined,
      src: undefined,
    },
    tags: {},
    labels: [],
    timestamp: undefined,
  },
  init: async (id: string) => {
    return getTag(id).then((response: any) => {
      for (let key in response.data) {
        videoState.data[key] = response.data[key];
      }
      return response.data;
    });
  },
  reset: async () => {
    return videoState.init(videoState.data.id);
  },
  getTimestamp: () => {
    return getDatetime(videoState.data.timestamp);
  },
  save: async () => {
    for (const attr in videoState.data.attributes) {
      if (typeof videoState.data.attributes[attr] === "string") {
        if (videoState.data.attributes[attr].length === 0) {
          videoState.data.attributes[attr] = null;
        } else {
          videoState.data.attributes[attr] = videoState.data.attributes[attr].trim();
        }
      }
    }
    const emptyTagFields = [];
    for (const field in videoState.data.tags) {
      if (videoState.data.tags[field] === undefined || videoState.data.tags[field].length === 0) {
        emptyTagFields.push(field);
      }
    }
    for (const field of emptyTagFields) {
      delete videoState.data.tags[field];
    }
    return postTag(videoState.data.id, videoState.data)
      .then((response) => {
        if (response.status === 200) {
          videoState.reset();
        }
        return response.data;
      })
      .catch((error) => {
        const code = error.response.status;
        const detail = error.response.data.detail;
        if (detail !== undefined) {
          messageState.push(detail);
        } else {
          messageState.push(error);
        }
        return Promise.reject(error);
      });
  },
});
