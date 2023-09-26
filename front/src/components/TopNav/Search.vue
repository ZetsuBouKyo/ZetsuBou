<script setup lang="ts">
import { onBeforeMount, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownOption, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";
import { SearchAnalyzer, SearchBase, SearchBoolean, SearchCategory, SearchState } from "@/interface/search";
import {
  AdvancedSearchField,
  AdvancedSearchFieldKeyEnum,
  AdvancedSearchFieldType,
  AdvancedSearchState,
} from "./AdvancedSearch/interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Dropdown from "@/elements/Dropdown/Dropdown.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import AdvancedSearch from "./AdvancedSearch/index.vue";
import SearchAutoComplete from "./SearchAutoComplete.vue";

import { getUserElasticSearchQueries } from "@/api/v1/user/elasticQuery/search";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { userState } from "@/state/user";

import { detectRouteChange } from "@/utils/route";
import { toTitle } from "@/utils/str";

const route = useRoute();
const router = useRouter();

const state = reactive<SearchState>({
  query: {
    query_id: undefined,
    page: 1,
    size: undefined,
    analyzer: undefined,
    boolean: SearchBoolean.Should,
    fuzziness: undefined,
    keywords: route.query.keywords as string,
    seed: undefined,
  },
  category: route.meta.search as SearchCategory,
  searchBase: route.meta.base as SearchBase,
  defaultKeywords: route.query.keywords as string,
  advancedSearchState: { fields: [], category: SearchCategory.Gallery },
  width: undefined,
  isOptions: undefined,
  show: undefined,
});

const advancedSearch = ref();
function advanced() {
  advancedSearch.value.open();
}

const searchAutoComplete = ref();
function openSearchAutoComplete() {
  searchAutoComplete.value.open();
}
function closeSearchAutoComplete() {
  if (searchAutoComplete.value === null) {
    return;
  }
  if (searchAutoComplete.value.isOpened()) {
    focusInput();
  }
  searchAutoComplete.value.close();
}
watch(
  () => searchAutoComplete.value?.isOpened(),
  () => {
    if (searchAutoComplete.value?.isOpened()) {
      state.isOptions = true;
    } else {
      state.isOptions = false;
    }
  },
);

const searchInput = ref();
function focusInput() {
  searchInput.value.focus();
}
watch(
  () => state.query?.keywords,
  () => {
    if (!state.query?.keywords) {
      return;
    }
    openSearchAutoComplete();
    focusInput();
  },
);
watch(
  () => searchInput.value?.getBoundingClientRect() + String(searchAutoComplete),
  () => {
    const rect = searchInput.value?.getBoundingClientRect();
    if (rect === undefined || searchAutoComplete?.value === undefined) {
      return;
    }
    state.width = rect.width;
  },
);
onBeforeMount(() => {
  document.addEventListener.call(window, "resize", () => {
    const rect = searchInput.value?.getBoundingClientRect();
    if (rect === undefined || searchAutoComplete?.value === undefined) {
      return;
    }
    state.width = rect.width;
  });
});

const queryTypeState = initSelectDropdownState() as SelectDropdownState;
queryTypeState.options = [
  { title: toTitle(SearchBase.Search), value: SearchBase.Search },
  { title: toTitle(SearchBase.Random), value: SearchBase.Random },
];
watch(
  () => queryTypeState.selectedValue,
  () => {
    state.searchBase = queryTypeState.selectedValue as SearchBase;
    if (queryTypeState.selectedValue !== undefined) {
      customSearchState.clear();
    } else {
      state.searchBase = SearchBase.Search;
    }
  },
);

const analyzerState = initSelectDropdownState() as SelectDropdownState;
const elasticAnalyzers = Object.values(SearchAnalyzer);
for (let analyzer of elasticAnalyzers) {
  analyzerState.options.push({ title: toTitle(analyzer), value: analyzer });
}
watch(
  () => analyzerState.selectedValue,
  () => {
    state.query.analyzer = analyzerState.selectedValue as SearchAnalyzer;
    if (analyzerState.selectedValue !== undefined) {
      customSearchState.clear();
    }
  },
);

const fuzzinessState = initSelectDropdownState() as SelectDropdownState;
fuzzinessState.options = [
  { title: 0, value: 0 },
  { title: 1, value: 1 },
  { title: 2, value: 2 },
  { title: 3, value: 3 },
];
watch(
  () => fuzzinessState.selectedValue,
  () => {
    state.query.fuzziness = fuzzinessState.selectedValue as number;
    if (fuzzinessState.selectedValue !== undefined) {
      customSearchState.clear();
    }
  },
);

const booleanTypeState = initSelectDropdownState() as SelectDropdownState;
booleanTypeState.options = [
  { title: toTitle(SearchBoolean.Should), value: SearchBoolean.Should },
  { title: toTitle(SearchBoolean.Must), value: SearchBoolean.Must },
];
watch(
  () => booleanTypeState.selectedValue,
  () => {
    state.query.boolean = booleanTypeState.selectedValue as SearchBoolean;
    if (booleanTypeState.selectedValue !== undefined) {
      customSearchState.clear();
    }
  },
);

function resetGeneralSearchQuery() {
  state.query.analyzer = undefined;
  state.query.boolean = undefined;
  state.query.fuzziness = undefined;
  state.query.keywords = undefined;
  state.query.seed = undefined;
}

function updateSearchQuery() {
  state.query.page = 1;

  if (route.query.size) {
    state.query.size = Number(route.query.size);
  }

  if (route.query.query_id) {
    return;
  }

  resetGeneralSearchQuery();

  if (route.query.analyzer) {
    state.query.analyzer = route.query.analyzer as any;
    analyzerState.title = toTitle(state.query.analyzer);
    analyzerState.selectedValue = state.query.analyzer;
  }

  if (route.query.boolean) {
    state.query.boolean = route.query.boolean as any;
    booleanTypeState.title = toTitle(state.query.boolean);
    booleanTypeState.selectedValue = state.query.boolean;
  }

  if (route.query.fuzziness) {
    state.query.fuzziness = Number(route.query.fuzziness);
    fuzzinessState.title = state.query.fuzziness;
    fuzzinessState.selectedValue = state.query.fuzziness;
  }

  if (route.query.keywords) {
    state.query.keywords = route.query.keywords as string;
  }

  if (route.query.seed) {
    state.query.seed = Number(route.query.seed);
  }
}

function updateGalleryAdvancedSearchState() {
  state.advancedSearchState.fields = <Array<AdvancedSearchField>>[
    {
      name: "keywords",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.BuiltIn,
      type: AdvancedSearchFieldType.String,
    },
    {
      name: "name",
      key: "name",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
      type: AdvancedSearchFieldType.String,
    },
    {
      name: "raw_name",
      key: "raw_name",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
      type: AdvancedSearchFieldType.String,
    },
    {
      name: "src",
      key: "src",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
      type: AdvancedSearchFieldType.String,
    },
    {
      name: "path",
      key: "path",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
      type: AdvancedSearchFieldType.String,
    },
    { name: "rating", value: undefined, type: AdvancedSearchFieldType.Range, gte: undefined, lte: undefined },
  ];
}

function updateVideoAdvancedSearchState() {
  state.advancedSearchState.fields = <Array<AdvancedSearchField>>[
    {
      name: "keywords",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.BuiltIn,
      type: AdvancedSearchFieldType.String,
    },
    {
      name: "name",
      key: "name",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
      type: AdvancedSearchFieldType.String,
    },
    {
      name: "other_names",
      key: "other_names",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
      type: AdvancedSearchFieldType.String,
    },
    {
      name: "src",
      key: "src",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
      type: AdvancedSearchFieldType.String,
    },
    {
      name: "path",
      key: "path",
      value: undefined,
      keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
      type: AdvancedSearchFieldType.String,
    },
    { name: "rating", value: undefined, type: AdvancedSearchFieldType.Range, gte: undefined, lte: undefined },
    { name: "height", value: undefined, type: AdvancedSearchFieldType.Range, gte: undefined, lte: undefined },
    { name: "width", value: undefined, type: AdvancedSearchFieldType.Range, gte: undefined, lte: undefined },
    { name: "duration", value: undefined, type: AdvancedSearchFieldType.Duration, gte: undefined, lte: undefined },
  ];
}

function updateByPath(path: string) {
  if (path === undefined) {
    return;
  }

  state.show = route.meta.search === SearchCategory.Gallery || route.meta.search === SearchCategory.Video;
  if (!state.show) {
    return;
  }

  state.searchBase = route.meta.base as SearchBase;
  const searchBase = Object.values(SearchBase);
  if (searchBase.includes(state.searchBase)) {
    queryTypeState.title = toTitle(state.searchBase);
    queryTypeState.selectedValue = state.searchBase;
  }

  updateSearchQuery();

  state.category = route.meta.search as SearchCategory;
  state.advancedSearchState = { fields: [], category: state.category } as AdvancedSearchState;

  switch (state.category) {
    case SearchCategory.Gallery:
      updateGalleryAdvancedSearchState();
      break;
    case SearchCategory.Video:
      updateVideoAdvancedSearchState();
      break;
  }
}

updateByPath(route.path);
watch(
  () => detectRouteChange(route),
  (path, _) => {
    if (route.path.endsWith("advanced-search")) {
      reset();
    } else {
      updateByPath(path);
    }
  },
);

function search() {
  if (state.query.query_id !== undefined) {
    resetGeneralSearchQuery();
  }
  let url = `/${state.category}/${state.searchBase}`;
  let queries = [];
  if (!state.query?.page) {
    queries.push("page=1");
  }

  if (state.searchBase === SearchBase.Random) {
    queries.push("seed=" + Math.floor(Math.random() * 100000000).toString());
  }

  for (let key in state.query) {
    if (state.query[key] !== undefined) {
      queries.push(`${key}=${encodeURIComponent(state.query[key])}`);
    }
  }
  if (queries.length > 0) {
    url += "?";
    url += queries.join("&");
  }
  window.scrollTo(0, 0);
  router.push(url);
  closeSearchAutoComplete();
  dropdown.value.close();
}
const customSearchState = initSelectDropdownState() as SelectDropdownState;

const userID = userState.data.id;
function onGet(params: PaginationGetParam) {
  return getUserElasticSearchQueries(userID, params);
}
function onGetToOptions(data: { name: string | number; id: number }) {
  return { title: data.name, value: data.id };
}
function onGetTip(opt: SelectDropdownOption) {
  return opt.title as string;
}

watch(
  () => customSearchState.selectedValue,
  () => {
    state.query.query_id = customSearchState.selectedValue as number;
    if (customSearchState.selectedValue !== undefined) {
      analyzerState.clear();
      queryTypeState.clear();
      booleanTypeState.clear();
    }
  },
);

const dropdown = ref();

const analyzer = ref();
const fuzziness = ref();
const query = ref();
const bool = ref();
const custom = ref();

function onClick() {
  try {
    analyzer.value.close();
    fuzziness.value.close();
    query.value.close();
    bool.value.close();
    custom.value.close();
  } catch (e: any) {
    if (e.name !== "TypeError") {
      throw e;
    }
  }
}

function clearAll() {
  analyzerState.clear();
  fuzzinessState.clear();
  queryTypeState.clear();
  booleanTypeState.clear();
  customSearchState.clear();
}

function reset() {
  state.query.keywords = undefined;
  clearAll();
}
</script>

<template>
  <advanced-search ref="advancedSearch" :key="state.category" :state="state.advancedSearchState"></advanced-search>
  <div class="sm:mr-5 mr-2 relative ml-4 flex w-full 3xl:text-base text-sm">
    <input
      ref="searchInput"
      class="w-full border-l-4 border-r-0 border-t-0 border-b-0 border-gray-700 bg-gray-700 text-white placeholder-gray-400 h-10 pl-2 pr-16 focus:border-gray-700 focus:ring-transparent inline-block"
      :class="state.isOptions ? 'rounded-t-lg' : 'rounded-lg'"
      type="text"
      v-if="state.show"
      v-model="state.query.keywords"
      @keypress.enter="search"
      @click="openSearchAutoComplete"
      @focusout="closeSearchAutoComplete" />
    <search-auto-complete ref="searchAutoComplete" :width="state.width" :search-state="state" />
    <div class="absolute right-0 h-full inline-flex text-left" v-if="state.show">
      <button type="button" class="flex flex-row items-center w-full mr-1 font-medium text-gray-700 focus:outline-none">
        <icon-ic-baseline-search class="hover:opacity-50" style="font-size: 1.5rem; color: white" @click="search" />
      </button>
      <dropdown
        ref="dropdown"
        class="mr-1"
        :options-width-class="'w-80'"
        :options-overflow-y-class="''"
        :on-click="onClick">
        <template v-slot:options>
          <div class="flex flex-col py-1">
            <div class="modal-row h-10">
              <span class="w-24 mr-4">Base:</span>
              <select-dropdown
                ref="query"
                class="w-44 flex-1"
                :group="'search'"
                :options-width-class="'w-44'"
                :origin="Origin.BottomLeft"
                :state="queryTypeState" />
            </div>
            <div class="modal-row h-10">
              <span class="w-24 mr-4">Analyzer:</span>
              <select-dropdown
                ref="analyzer"
                class="w-44 flex-1"
                :group="'search'"
                :options-width-class="'w-44'"
                :origin="Origin.BottomLeft"
                :state="analyzerState" />
            </div>
            <div class="modal-row h-10">
              <span class="w-24 mr-4">Fuzziness:</span>
              <select-dropdown
                ref="fuzziness"
                class="w-44 flex-1"
                :group="'search'"
                :options-width-class="'w-44'"
                :origin="Origin.BottomLeft"
                :state="fuzzinessState" />
            </div>
            <div class="modal-row h-10">
              <span class="w-24 mr-4">Boolean:</span>
              <select-dropdown
                ref="bool"
                class="w-44 flex-1"
                :group="'search'"
                :options-width-class="'w-44'"
                :origin="Origin.BottomLeft"
                :state="booleanTypeState" />
            </div>
            <div class="modal-row h-10">
              <span class="w-24 mr-4">Custom:</span>
              <select-dropdown
                ref="custom"
                class="w-44 flex-1"
                :group="'search'"
                :options-width-class="'w-44'"
                :origin="Origin.BottomLeft"
                :state="customSearchState"
                :on-get="onGet"
                :on-get-to-options="onGetToOptions"
                :on-get-tip="onGetTip" />
            </div>
            <div class="modal-row">
              <ripple-button class="btn-dark w-full h-10" @click="clearAll">Clear</ripple-button>
            </div>
            <div class="modal-row">
              <ripple-button class="btn-dark w-full h-10" @click="advanced">Advanced</ripple-button>
            </div>
            <div class="modal-row">
              <ripple-button class="btn-dark w-full h-10" @click="search">Search</ripple-button>
            </div>
          </div>
        </template>
      </dropdown>
    </div>
  </div>
</template>
