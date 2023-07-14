import { Pagination } from "@/elements/Pagination/pagination.interface";

export interface Item {
  category?: string;
  rating?: number;
  title?: string;
  imgUrl: string;
  linkUrl: string;
  srcUrl?: string;
  timestamp?: string;
}

export interface Items extends Array<Item> {}

export interface Previews {
  items: Items;
  pagination: Pagination;
}
