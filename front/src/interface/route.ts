import { RouteLocationNormalizedLoaded } from "vue-router";

import { DataState } from "./state";

export interface RouteData {
    route: RouteLocationNormalizedLoaded;
    watchSources: () => any;
    load: () => void;
}

export interface _RouteState<DataT> extends DataState<DataT> {
    setRoute: (r: RouteLocationNormalizedLoaded) => void;
    setWatchSources: (f: () => any) => void;
    setLoadFunction: (f: () => void) => void;
}

export type RouteState = _RouteState<RouteData>;
