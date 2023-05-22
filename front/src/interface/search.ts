export enum SearchAnalyzer {
  default = "default",
  keyword = "keyword",
  ngram = "ngram",
  standard = "standard",
  url = "url",
}

export enum SearchBase {
  Search = "search",
  Random = "random",
  AdvancedSearch = "advanced-search",
}

export enum SearchCategory {
  Gallery = "gallery",
  Video = "video",
}

export enum SearchBoolean {
  Must = "must",
  Should = "should",
}

export interface SearchStateQuery {
  analyzer?: SearchAnalyzer;
  query_id?: number;
  keywords?: string;
  page?: number;
  fuzziness?: number;
  size?: number;
  boolean?: SearchBoolean;
  seed?: number;
}

export interface SearchState {
  query: SearchStateQuery;
  category: SearchCategory;
  searchBase: SearchBase;
  defaultKeywords: string;
  autocomplete: string;
  advancedSearchState: any;
}
