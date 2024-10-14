import { reactive } from "vue";

import { Gallery } from "@/interface/gallery";
import { SourceState } from "@/interface/state";

import { getGalleryTag, postGalleryTag } from "@/api/v1/gallery/tag";

import { getDatetime } from "@/utils/datetime";
import { cleanData } from "@/utils/source";

export const galleryState = reactive<SourceState<Gallery>>({
    data: {
        id: undefined,
        path: undefined,
        name: undefined,
        raw_name: undefined,
        other_names: undefined,
        last_updated: undefined,
        upload_date: undefined,
        src: [],
        labels: [],
        tags: {},
        attributes: {
            category: null,
            rating: null,
            uploader: null,
            pages: null,
        },
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
    getLastUpdated: () => {
        return getDatetime(galleryState.data.last_updated);
    },
    save: async (successEvent) => {
        if (galleryState.data.id === undefined) {
            return;
        }

        cleanData(galleryState);

        return postGalleryTag(galleryState.data.id, galleryState.data).then((response) => {
            if (response.status === 200) {
                galleryState.reset();
            }
            if (successEvent) {
                successEvent(response);
            }
            return response;
        });
    },
});
