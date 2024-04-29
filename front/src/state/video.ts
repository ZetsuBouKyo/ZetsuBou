import { reactive } from "vue";

import { Video } from "@/interface/video";
import { SourceState } from "@/interface/state";

import { getTag, postTag } from "@/api/v1/video/tag";
import { getDatetime } from "@/utils/datetime";
import { cleanData } from "@/utils/source";

import { messageState } from "./message";
import { viewDepthKey } from "vue-router";

export const videoState = reactive<SourceState<Video>>({
    data: {
        id: undefined,
        path: undefined,
        name: undefined,
        other_names: [],
        src: undefined,
        last_updated: undefined,
        labels: [],
        tags: {},
        attributes: {
            category: undefined,
            rating: undefined,
            uploader: undefined,
            height: undefined,
            width: undefined,
            duration: undefined,
            fps: undefined,
            frames: undefined,
            md5: undefined,
        },
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
    getLastUpdated: () => {
        return getDatetime(videoState.data.last_updated);
    },
    save: async (successEvent) => {
        if (videoState.data.id === undefined) {
            return;
        }

        cleanData(videoState);

        return postTag(videoState.data.id, videoState.data).then((response) => {
            if (response.status === 200) {
                videoState.reset();
            }
            successEvent(response);
            return response.data;
        });
    },
});
