export interface PaginationGetParam {
    page?: number;
    size?: number;
    is_desc?: boolean;
}

export interface Page {
    n: number;
    link: string;
}

export interface Pagination {
    totalPage: number;
    totalItems: number;
    current: number;
    path: string;
    pages: Array<Page>;
    perRound: number;
    query: any;
    toLastPage?: string;
    toFirstPage?: string;
    toNextPage?: string;
    toPreviousPage?: string;
}
