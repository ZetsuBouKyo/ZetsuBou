export interface Query {
  size: number;
  page: string | number;
}

export interface Page {
  n: number;
  link: string;
}

export interface Pagination {
  totalPage: number;
  totalItems: number;
  current: number;
  pages: Array<Page>;
  perRound: number;
  toLastPage?: string;
  toFirstPage?: string;
  toNextPage?: string;
  toPreviousPage?: string;
}
