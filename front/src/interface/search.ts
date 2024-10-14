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

export interface SearchQuery {
    analyzer: string;
    query_id: number;
    keywords: string;
    page: number;
    fuzziness: number;
    size: number;
    boolean: "must" | "should";
    seed?: number;
    [key: string]: any;
}

export interface SearchStateQuery {
    query_id?: number;
    page?: number;
    size?: number;
    analyzer?: SearchAnalyzer;
    boolean?: SearchBoolean;
    fuzziness?: number;
    keywords?: string;
    seed?: number;
}

export interface SearchState {
    query: SearchStateQuery;
    category: SearchCategory;
    searchBase: SearchBase;
    defaultKeywords: string;
    advancedSearchState: any;
    width: number;
    isOptions: boolean;
    show: boolean;
}
