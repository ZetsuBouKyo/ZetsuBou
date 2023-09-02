import { reactive, watch } from "vue";
import { RouteLocationNormalizedLoaded } from "vue-router";

import { PreviewsState, PreviewsData } from "./interface";

import { detectRouteChange } from "@/utils/route";

export const previewsState = reactive<PreviewsState<PreviewsData>>({
  data: {
    route: undefined,
    watchSources: undefined,
    load: undefined,
  },
  pagination: undefined,
  items: undefined,
  setRoute: (r: RouteLocationNormalizedLoaded) => {
    previewsState.data.route = r;
  },
  setWatchSources: (f: () => any) => {
    previewsState.data.watchSources = f;
  },
  setLoadFunction: (f: (state: PreviewsState<PreviewsData>) => void) => {
    previewsState.data.load = f;
  },
});

watch(
  () => {
    const w = [];
    const route = previewsState.data.route;
    if (route !== undefined) {
      w.push(detectRouteChange(route));
    }
    const watchSources = previewsState.data.watchSources;
    if (watchSources !== undefined) {
      w.push(watchSources());
    }
    return w;
  },
  () => {
    const load = previewsState.data.load;
    if (load === undefined) {
      return;
    }
    load(previewsState);
  },
);
