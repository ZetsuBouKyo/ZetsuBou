import { reactive } from "vue";

import { SearchQuery } from "@/interface/search";

export interface Page {
  total: Number;
  current: Number;
  query: SearchQuery;
  totalItems?: Number;
  pages?: Array<String>;
  perRound?: Number;
}

export interface Item {
  category: String;
  title: String;
  imgUrl: String;
  linkUrl: String;
}

export interface Items extends Array<Item> {}

export interface Previews {
  items: Items;
  page: Page;
}

export interface PreviewsState {
  data: Previews;
  init: Function;
  reset: Function;
}

export const previewsState = reactive<PreviewsState>({
  data: {
    items: undefined,
    page: undefined,
  },
  init: (items: Items, page: Page) => {
    previewsState.data.items = items;
    previewsState.data.page = page;
  },
  reset: () => {
    previewsState.data.items = undefined;
    previewsState.data.page = undefined;
  },
});
