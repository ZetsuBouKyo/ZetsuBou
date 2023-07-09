import { Pagination, Page, PaginationGetParam } from "./pagination.d";

function getPageUrl(page: number, path: string, query: PaginationGetParam) {
  let paras = [];
  for (let key in query) {
    if (query[key] !== undefined) {
      if (key !== "page") {
        paras.push(`${key}=${query[key]}`);
      }
    }
  }

  paras.push("page=" + page.toString());
  if (paras.length > 0) {
    path += "?" + paras.join("&");
  }
  return path;
}

export function getPagination(path: string, totalItems: number, query: PaginationGetParam) {
  query.page = parseInt(query.page.toString());
  query.size = parseInt(query.size.toString());

  const totalPage = Math.ceil(totalItems / (query.size as number));
  if (totalPage === 0) {
    return undefined;
  }
  const current = query.page as number;
  if (isNaN(current)) {
    return undefined;
  }

  const pagination: Pagination = {
    totalPage: totalPage,
    totalItems: totalItems,
    current: current,
    pages: [],
    perRound: 6,
    toLastPage: getPageUrl(totalPage, path, query),
    toFirstPage: getPageUrl(1, path, query),
    toNextPage: getPageUrl(current + 1, path, query),
    toPreviousPage: getPageUrl(current - 1, path, query),
  };

  if (pagination.totalPage <= pagination.perRound) {
    for (let i = 1; i < pagination.totalPage + 1; i++) {
      const page: Page = {
        n: i,
        link: getPageUrl(i, path, query),
      };
      pagination.pages.push(page);
    }
  } else {
    let startPage = Math.max(1, pagination.current - 1);
    let endPage = Math.min(pagination.totalPage, startPage + pagination.perRound - 1);
    if (endPage - startPage + 1 < pagination.perRound) {
      startPage = Math.min(startPage, endPage - pagination.perRound + 1);
      startPage = Math.max(startPage, 1);
    }
    for (let i = startPage; i < endPage + 1; i++) {
      const page: Page = {
        n: i,
        link: getPageUrl(i, path, query),
      };
      pagination.pages.push(page);
    }
  }
  return pagination;
}
