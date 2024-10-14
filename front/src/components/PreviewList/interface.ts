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
