<template>
  <advanced-search ref="advancedSearch" :state="state.advancedSearchState"></advanced-search>
  <div class="sm:mr-5 mr-2 relative ml-4 flex w-full 3xl:text-base text-sm">
    <input
      class="w-full border-2 border-gray-600 bg-gray-700 text-white placeholder-gray-400 h-10 pl-2 pr-16 rounded-lg focus:outline-none hidden sm:inline-block"
      type="text"
      v-model="state.query.keywords"
      @keypress.enter="search"
      v-if="state.defaultKeywords"
      :list="state.autocomplete"
    />
    <input
      class="w-full border-2 border-gray-600 bg-gray-700 text-white placeholder-gray-400 h-10 pl-2 pr-16 rounded-lg focus:outline-none hidden sm:inline-block"
      type="text"
      placeholder="Search"
      v-model="state.query.keywords"
      @keypress.enter="search"
      v-else
      :list="state.autocomplete"
    />
    <input
      class="w-full border-2 border-gray-300 bg-white h-10 pl-2 pr-16 rounded-lg focus:outline-none inline-block sm:hidden"
      type="search"
      v-model="state.query.keywords"
      @keypress.enter="search"
      :list="state.autocomplete"
    />
    <search-auto-complete :id="state.autocomplete" :search-state="state" />
    <div class="absolute right-0 h-full inline-flex text-left">
      <button type="button" class="flex flex-row items-center w-full mr-1 font-medium text-gray-700 focus:outline-none">
        <icon-ic-baseline-search class="hover:opacity-50" style="font-size: 1.5rem; color: white" @click="search" />
      </button>
      <dropdown class="mr-1" :options-width-class="'w-80'" :options-overflow-y-class="''" :on-click="onClick">
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
                :state="queryTypeState"
              />
            </div>
            <div class="modal-row h-10">
              <span class="w-24 mr-4">Analyzer:</span>
              <select-dropdown
                ref="analyzer"
                class="w-44 flex-1"
                :group="'search'"
                :options-width-class="'w-44'"
                :origin="Origin.BottomLeft"
                :state="analyzerState"
              />
            </div>
            <div class="modal-row h-10">
              <span class="w-24 mr-4">Fuzziness:</span>
              <select-dropdown
                ref="fuzziness"
                class="w-44 flex-1"
                :group="'search'"
                :options-width-class="'w-44'"
                :origin="Origin.BottomLeft"
                :state="fuzzinessState"
              />
            </div>
            <div class="modal-row h-10">
              <span class="w-24 mr-4">Boolean:</span>
              <select-dropdown
                ref="bool"
                class="w-44 flex-1"
                :group="'search'"
                :options-width-class="'w-44'"
                :origin="Origin.BottomLeft"
                :state="booleanTypeState"
              />
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
                :on-get-tip="onGetTip"
              />
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

<script lang="ts">
import { useRoute } from "vue-router";
import { reactive, ref, watch } from "vue";

import { SearchAnalyzer, SearchBase, SearchBoolean, SearchCategory, SearchState } from "@/interface/search";

import { userState } from "@/state/user";

import { getUserElasticSearchQueries } from "@/api/v1/user/elasticQuery/search";

import Dropdown from "@/elements/Dropdown/Dropdown.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";
import SearchAutoComplete from "./SearchAutoComplete.vue";
import SelectDropdown, {
  GetParam,
  SelectDropdownMode,
  SelectDropdownOption,
  SelectDropdownState,
  Origin,
  clear,
} from "@/elements/Dropdown/SelectDropdown.vue";

import AdvancedSearch, {
  AdvancedSearchField,
  AdvancedSearchFieldKeyEnum,
  AdvancedSearchFieldType,
  AdvancedSearchState,
} from "./AdvancedSearch.vue";
import { toTitle } from "@/utils/str";

export default {
  components: { AdvancedSearch, Dropdown, RippleButton, SearchAutoComplete, SelectDropdown },
  setup() {
    const route = useRoute();

    const advancedSearch = ref();
    function advanced() {
      advancedSearch.value.open();
    }

    const state = reactive<SearchState>({
      query: {
        analyzer: undefined,
        query_id: undefined,
        keywords: route.query.keywords as string,
        page: 1,
        fuzziness: undefined,
        size: undefined,
        boolean: SearchBoolean.Should,
        seed: undefined,
      },
      category: SearchCategory.Gallery,
      searchBase: SearchBase.Search,
      defaultKeywords: route.query.keywords as string,
      autocomplete: "tag",
      advancedSearchState: { fields: [], category: SearchCategory.Gallery },
    });

    function updateByPath(path: string) {
      if (path === undefined) {
        return;
      }

      state.category = SearchCategory.Gallery;
      state.advancedSearchState = { fields: [], category: state.category } as AdvancedSearchState;

      const p = path.split("/");
      if (p.length > 1 && (p[1] === SearchCategory.Video || p[1] === "v")) {
        state.category = SearchCategory.Video;
        state.advancedSearchState.category = state.category;
        state.advancedSearchState.fields = <Array<AdvancedSearchField>>[
          {
            name: "keywords",
            keyType: AdvancedSearchFieldKeyEnum.BuiltIn,
            type: AdvancedSearchFieldType.String,
          },
          {
            name: "name",
            key: "name",
            keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
            type: AdvancedSearchFieldType.String,
          },
          {
            name: "other_names",
            key: "other_names",
            keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
            type: AdvancedSearchFieldType.String,
          },
          { name: "rating", type: AdvancedSearchFieldType.Range },
          { name: "height", type: AdvancedSearchFieldType.Range },
          { name: "width", type: AdvancedSearchFieldType.Range },
          { name: "duration", type: AdvancedSearchFieldType.Duration },
        ];
        return;
      }

      state.advancedSearchState.fields = <Array<AdvancedSearchField>>[
        {
          name: "keywords",
          keyType: AdvancedSearchFieldKeyEnum.BuiltIn,
          type: AdvancedSearchFieldType.String,
        },
        {
          name: "name",
          key: "attributes.name",
          keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
          type: AdvancedSearchFieldType.String,
        },
        {
          name: "raw_name",
          key: "attributes.raw_name",
          keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
          type: AdvancedSearchFieldType.String,
        },
        {
          name: "src",
          key: "attributes.src",
          keyType: AdvancedSearchFieldKeyEnum.ElasticsearchField,
          type: AdvancedSearchFieldType.String,
        },
        { name: "rating", type: AdvancedSearchFieldType.Range },
      ];
    }

    updateByPath(route.path);
    watch(
      () => route.path,
      (path, _) => {
        updateByPath(path);
      },
    );

    function search() {
      if (state.query.query_id !== undefined) {
        state.query.analyzer = undefined;
        state.query.keywords = undefined;
        state.query.fuzziness = undefined;
        state.query.boolean = undefined;
        state.query.seed = undefined;
      }
      let url = `/${state.category}/${state.searchBase}`;
      let queries = [];

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
      window.open(url, "_self");
    }
    const customSearchState = SelectDropdown.initState() as SelectDropdownState;

    const analyzerState = SelectDropdown.initState() as SelectDropdownState;
    const elasticAnalyzers = Object.values(SearchAnalyzer);
    for (let analyzer of elasticAnalyzers) {
      analyzerState.options.push({ title: toTitle(analyzer), value: analyzer });
    }

    watch(
      () => analyzerState.selectedValue,
      () => {
        state.query.analyzer = analyzerState.selectedValue as SearchAnalyzer;
        if (analyzerState.selectedValue !== undefined) {
          clear(customSearchState);
        }
      },
    );

    const fuzzinessState = SelectDropdown.initState() as SelectDropdownState;
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
          clear(customSearchState);
        }
      },
    );

    const queryTypeState = SelectDropdown.initState() as SelectDropdownState;
    queryTypeState.options = [
      { title: "Search", value: SearchBase.Search },
      { title: "Random", value: SearchBase.Random },
    ];
    watch(
      () => queryTypeState.selectedValue,
      () => {
        state.searchBase = queryTypeState.selectedValue as SearchBase;
        if (queryTypeState.selectedValue !== undefined) {
          clear(customSearchState);
        } else {
          state.searchBase = SearchBase.Search;
        }
      },
    );

    const booleanTypeState = SelectDropdown.initState() as SelectDropdownState;
    booleanTypeState.options = [
      { title: "Should", value: "should" },
      { title: "Must", value: "must" },
    ];
    watch(
      () => booleanTypeState.selectedValue,
      () => {
        state.query.boolean = booleanTypeState.selectedValue as SearchBoolean;
        if (booleanTypeState.selectedValue !== undefined) {
          clear(customSearchState);
        }
      },
    );

    const userID = userState.id;
    function onGet(params: GetParam) {
      return getUserElasticSearchQueries(userID, params);
    }
    function onGetToOptions(data: { name: string | number; id: number }) {
      return { title: data.name, value: data.id };
    }
    function onGetTip(opt: SelectDropdownOption) {
      return opt.title;
    }

    watch(
      () => customSearchState.selectedValue,
      () => {
        state.query.query_id = customSearchState.selectedValue as number;
        if (customSearchState.selectedValue !== undefined) {
          clear(analyzerState);
          clear(queryTypeState);
          clear(booleanTypeState);
        }
      },
    );

    const analyzer = ref();
    const fuzziness = ref();
    const query = ref();
    const bool = ref();
    const custom = ref();

    function onClick() {
      analyzer.value.close();
      fuzziness.value.close();
      query.value.close();
      bool.value.close();
      custom.value.close();
    }

    function clearAll() {
      clear(analyzerState);
      clear(fuzzinessState);
      clear(queryTypeState);
      clear(booleanTypeState);
      clear(customSearchState);
    }

    return {
      advancedSearch,
      advanced,
      Origin,
      SelectDropdownMode,
      analyzerState,
      fuzzinessState,
      queryTypeState,
      booleanTypeState,
      state,
      search,
      customSearchState,
      onGet,
      onGetToOptions,
      onGetTip,
      analyzer,
      fuzziness,
      query,
      bool,
      custom,
      onClick,
      clearAll,
    };
  },
};
</script>
