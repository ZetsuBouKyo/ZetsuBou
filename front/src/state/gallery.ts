import { reactive } from "vue";

import { Gallery } from "@/interface/gallery";
import { SourceState } from "@/interface/source";
import { getGalleryTag, postGalleryTag } from "@/api/v1/gallery/tag";
import { getDatetime } from "@/utils/datetime";

import { messageState } from "./message";

export const galleryState = reactive<SourceState<Gallery>>({
  data: {
    id: undefined,
    path: undefined,
    group: undefined,
    timestamp: undefined,
    mtime: undefined,
    attributes: {
      name: null,
      raw_name: null,
      uploader: null,
      category: null,
      rating: null,
      src: null,
    },
    tags: {},
    labels: [],
  },
  init: async (id: string) => {
    return getGalleryTag(id).then((response: any) => {
      for (let key in response.data) {
        galleryState.data[key] = response.data[key];
      }
      return response.data;
    });
  },
  reset: async () => {
    return galleryState.init(galleryState.data.id);
  },
  getTimestamp: () => {
    return getDatetime(galleryState.data.timestamp);
  },
  save: async (successEvent) => {
    for (const attr in galleryState.data.attributes) {
      if (typeof galleryState.data.attributes[attr] === "string") {
        if (galleryState.data.attributes[attr].length === 0) {
          galleryState.data.attributes[attr] = null;
        } else {
          galleryState.data.attributes[attr] = galleryState.data.attributes[attr].trim();
        }
      }
    }
    const emptyTagFields = [];
    for (const field in galleryState.data.tags) {
      if (galleryState.data.tags[field] === undefined || galleryState.data.tags[field].length === 0) {
        emptyTagFields.push(field);
      }
    }
    for (const field of emptyTagFields) {
      delete galleryState.data.tags[field];
    }
    return postGalleryTag(galleryState.data.id, galleryState.data)
      .then((response) => {
        if (response.status === 200) {
          galleryState.reset();
        }
        successEvent(response);
        return response;
      })
      .catch((error) => {
        return messageState.pushError(error);
      });
  },
});
