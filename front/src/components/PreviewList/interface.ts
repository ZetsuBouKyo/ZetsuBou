import { RouteLocationNormalizedLoaded } from "vue-router";

import { DataState } from "@/interface/state";
import { Pagination } from "@/elements/Pagination/pagination.interface";

export interface Item {
  category?: string;
  rating?: number;
  title?: string;
  pages?: number;
  imgUrl: string;
  linkUrl: string;
  srcUrl?: string;
  lastUpdated?: string;
}

export interface Items extends Array<Item> {}

export interface Previews {
  items: Items;
  pagination: Pagination;
}

export interface PreviewsData {
  route: RouteLocationNormalizedLoaded;
  watchSources?: () => any;
  load?: (state: PreviewsState<PreviewsData>) => void;
}

export interface PreviewsState<PreviewsData> extends DataState<PreviewsData> {
  pagination?: Pagination;
  items?: Items;
  setRoute: (route: RouteLocationNormalizedLoaded) => void;
  setWatchSources: (f: () => any) => void;
  setLoadFunction: (f: (state: PreviewsState<PreviewsData>) => void) => void;
}
