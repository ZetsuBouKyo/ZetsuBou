import { reactive, watch } from "vue";
import { RouteLocationNormalizedLoaded } from "vue-router";

import { RouteState } from "@/interface/route";

import { detectRouteChange } from "@/utils/route";

export const routeState = reactive<RouteState>({
    data: {
        route: undefined,
        watchSources: undefined,
        load: undefined,
    },
    setRoute: (r: RouteLocationNormalizedLoaded) => {
        routeState.data.route = r;
    },
    setWatchSources: (f: () => any) => {
        routeState.data.watchSources = f;
    },
    setLoadFunction: (f: () => void) => {
        routeState.data.load = f;
    },
});

watch(
    () => {
        const w = [];
        const route = routeState.data.route;
        if (route !== undefined) {
            w.push(detectRouteChange(route));
        }
        const watchSources = routeState.data.watchSources;
        if (watchSources !== undefined) {
            w.push(watchSources());
        }
        return w;
    },
    () => {
        const load = routeState.data.load;
        if (load === undefined) {
            return;
        }
        load();
    },
);
