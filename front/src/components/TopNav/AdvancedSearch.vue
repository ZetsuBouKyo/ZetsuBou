<template>
  <modal
    ref="advancedSearch"
    :title="'Advanced Search'"
    class="w-1/2 top-12 left-1/4"
    :is-scrollable="true"
    @keyup.enter="search">
    <div class="flex flex-col" v-for="(field, i) in state.fields" :key="i">
      <div class="flex flex-col" v-if="field.type === AdvancedSearchFieldType.String">
        <div class="modal-row h-10">
          <span class="w-28 mr-4 text-white">{{ toTitle(field.name).replace("_", " ") }}:</span>
          <input class="modal-input flex-1" type="text" :placeholder="field.value" v-model="field.value" />
        </div>
        <div class="modal-row h-10">
          <span class="w-24 ml-auto mr-4">Fuzziness:</span>
          <select-dropdown
            class="w-20 mr-4"
            :group="'search'"
            :options-width-class="'w-20'"
            :origin="Origin.BottomLeft"
            :state="field.fuzziness" />
          <span class="w-16 mr-4">Analyzer:</span>
          <select-dropdown
            class="w-32 mr-4"
            :group="'search'"
            :options-width-class="'w-32'"
            :origin="Origin.BottomLeft"
            :state="field.analyzer" />
          <span class="w-16 mr-4">Boolean:</span>
          <select-dropdown
            class="w-28"
            :group="'search'"
            :options-width-class="'w-28'"
            :origin="Origin.BottomLeft"
            :state="field.boolean" />
        </div>
      </div>
      <div class="flex flex-col" v-else-if="field.type === AdvancedSearchFieldType.Range">
        <div class="modal-row h-10">
          <span class="w-28 mr-4 text-white">{{ toTitle(field.name) }}:</span>
          <input class="modal-input flex-1" type="text" :placeholder="field.gte" v-model="field.gte" />
          <span class="mx-4">to</span>
          <input class="modal-input flex-1" type="text" :placeholder="field.lte" v-model="field.lte" />
        </div>
      </div>
      <div class="flex flex-col" v-else-if="field.type === AdvancedSearchFieldType.Duration">
        <div class="modal-row h-10">
          <span class="w-28 mr-4 text-white">{{ toTitle(field.name) }}:</span>
          <input class="modal-input flex-1" type="text" :placeholder="field.gte" v-model="field.gte" />
          <span class="mx-4">to</span>
          <input class="modal-input flex-1" type="text" :placeholder="field.lte" v-model="field.lte" />
        </div>
      </div>
    </div>
    <div class="modal-row h-10">
      <span class="w-28 mr-4 text-white">Category:</span>
      <select-dropdown
        class="flex-1"
        :options-width-class="'w-96'"
        :origin="Origin.BottomLeft"
        :state="categories"
        :is-auto-complete="true"
        :on-get="onGetCategories"
        :on-get-to-options="onGetCategoriesToOptions"
        :on-get-tip="onGetTip"
        :on-mouseover-option="onMouseoverOption"
        :mode="SelectDropdownMode.Input" />
    </div>
    <div class="modal-row h-10">
      <span class="w-28 mr-4 text-white">Uploader:</span>
      <select-dropdown
        class="flex-1"
        :options-width-class="'w-96'"
        :origin="Origin.BottomLeft"
        :state="uploader"
        :is-auto-complete="true"
        :on-get="onGetUploader"
        :on-get-to-options="onGetUploaderToOptions"
        :on-get-tip="onGetTip"
        :on-mouseover-option="onMouseoverOption"
        :mode="SelectDropdownMode.Input" />
    </div>
    <div class="modal-row" @keyup.enter.stop="">
      <span class="w-28 mr-4 text-white">Labels:</span>
      <select-dropdown
        class="flex-1"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="labels"
        :on-get="getTagTokenStartWith"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.InputChips" />
    </div>
    <div class="modal-row" @keyup.enter.stop="">
      <span class="w-28 mr-4 text-white">Tag Fields:</span>
      <select-dropdown
        class="flex-1"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="tagFields"
        :on-get="getStartWithTagFields"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.InputChips" />
    </div>
    <div
      class="modal-row"
      v-for="(_, field) in privateState.tagFields"
      :key="privateState.tagFields[field]"
      @keyup.enter.stop="">
      <span class="w-28 mx-4">{{ field }}:</span>
      <select-dropdown
        class="flex-1"
        :is-input-chips-title-unique="true"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="privateState.tagFields[field]"
        :on-get="privateState.onGets[field]"
        :on-get-to-options="tokenToOption"
        :mode="SelectDropdownMode.InputChips" />
    </div>
    <div class="modal-row">
      <div class="flex ml-auto">
        <ripple-button class="flex btn btn-primary" @click="search"> Search </ripple-button>
      </div>
    </div>
  </modal>
</template>

<script lang="ts">
import { PropType, reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";

import {
  getSettingFrontGalleryStartWithCategories,
  getSettingFrontGalleryStartWithTagFields,
} from "@/api/v1/setting/front/gallery";
import {
  getSettingFrontVideoStartWithCategories,
  getSettingFrontVideoStartWithTagFields,
} from "@/api/v1/setting/front/video";
import { getTagTokenStartWith } from "@/api/v1/tag/token";

import { Source, SourceDataState } from "@/interface/source";
import { SearchCategory } from "@/interface/search";
import { TagFieldsPrivateState } from "@/interface/tag";

import { durationToSecond } from "@/utils/datetime";
import { toTitle } from "@/utils/str";
import { onGetTip, onMouseoverOption } from "@/utils/tag";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Modal from "@/elements/Modal/Modal.vue";

import SelectDropdown, {
  OnGet,
  Origin,
  SelectDropdownMode,
  SelectDropdownState,
} from "@/elements/Dropdown/SelectDropdown.vue";

import { settingState } from "@/state/setting";

import { watchLabels, watchLabelsChipsLength } from "@/utils/label";
import { watchTags, watchTagFieldsChipsLength } from "@/utils/tag";

export enum AdvancedSearchFieldType {
  String,
  Range,
  Duration,
}

export enum AdvancedSearchFieldKeyEnum {
  ElasticsearchField,
  BuiltIn,
}

export interface AdvancedSearchField {
  name: string;
  type: AdvancedSearchFieldType;
  key?: string;
  keyType?: AdvancedSearchFieldKeyEnum;
  value?: string;
  fuzziness?: SelectDropdownState;
  analyzer?: SelectDropdownState;
  boolean?: SelectDropdownState;
  gte?: number | string;
  lte?: number | string;
}

export interface AdvancedSearchState {
  category: SearchCategory;
  fields: Array<AdvancedSearchField>;
}

export default {
  components: { Modal, RippleButton, SelectDropdown },
  props: {
    state: {
      type: Object as PropType<AdvancedSearchState>,
      default: undefined,
    },
  },
  setup(props) {
    const router = useRouter();
    const state = props.state;

    const privateState = reactive<TagFieldsPrivateState>({
      tagFields: {},
      onGets: {},
    });
    const sourceState = reactive<SourceDataState<Source>>({
      data: { labels: [], tags: {} },
    });

    function load() {
      if (settingState.setting === undefined) {
        return;
      }

      for (const field of props.state.fields) {
        switch (field.type) {
          case AdvancedSearchFieldType.String:
            field.fuzziness = SelectDropdown.initState() as SelectDropdownState;
            field.fuzziness.options = [
              { title: 0, value: 0 },
              { title: 1, value: 1 },
              { title: 2, value: 2 },
              { title: 3, value: 3 },
            ];

            field.analyzer = SelectDropdown.initState() as SelectDropdownState;

            let analyzers: any;

            switch (field.keyType) {
              case AdvancedSearchFieldKeyEnum.BuiltIn:
                analyzers = settingState.setting[props.state.category].analyzer.keyword as object;
                for (let analyzer in analyzers) {
                  field.analyzer.options.push({ title: toTitle(analyzer), value: analyzer });
                }
                break;
              case AdvancedSearchFieldKeyEnum.ElasticsearchField:
                analyzers = settingState.setting[props.state.category].analyzer.field[field.key] as Array<string>;
                for (let analyzer of analyzers) {
                  field.analyzer.options.push({ title: toTitle(analyzer), value: analyzer });
                }
                break;
            }

            field.boolean = SelectDropdown.initState() as SelectDropdownState;
            field.boolean.options = [
              { title: "Should", value: "should" },
              { title: "Must", value: "must" },
            ];
            break;
        }
      }
    }
    load();

    watch(
      () => JSON.stringify(settingState.setting) + JSON.stringify(state.category),
      () => {
        load();
      },
    );

    let onGetCategories: OnGet;
    let getStartWithTagFields: OnGet;
    switch (state.category) {
      case SearchCategory.Gallery:
        onGetCategories = getSettingFrontGalleryStartWithCategories;
        getStartWithTagFields = getSettingFrontGalleryStartWithTagFields;
        break;
      case SearchCategory.Video:
        onGetCategories = getSettingFrontVideoStartWithCategories;
        getStartWithTagFields = getSettingFrontVideoStartWithTagFields;
    }

    const categories = SelectDropdown.initState() as SelectDropdownState;

    const onGetCategoriesToOptions = tokenToOption;

    const uploader = SelectDropdown.initState() as SelectDropdownState;
    const onGetUploader = getTagTokenStartWith;
    const onGetUploaderToOptions = tokenToOption;

    const advancedSearch = ref();

    const labels = SelectDropdown.initState() as SelectDropdownState;
    watch(...watchLabels(labels, sourceState));
    watch(...watchLabelsChipsLength(labels, sourceState));

    const tagFields = SelectDropdown.initState() as SelectDropdownState;
    watch(...watchTags(privateState, tagFields, sourceState));
    watch(...watchTagFieldsChipsLength(privateState, tagFields, sourceState));

    function search() {
      const queries = {};

      if (categories.title !== undefined) {
        queries["category"] = categories.title;
      }

      if (uploader.title !== undefined) {
        queries["uploader"] = uploader.title;
      }

      for (const field of props.state.fields) {
        if (field.name === undefined) {
          continue;
        }
        switch (field.type) {
          case AdvancedSearchFieldType.String:
            if (field.value === undefined) {
              break;
            }
            queries[field.name] = field.value;
            if (field.fuzziness.selectedValue !== undefined && Number.isInteger(field.fuzziness.selectedValue)) {
              queries[`${field.name}_fuzziness`] = field.fuzziness.selectedValue;
            }
            if (field.analyzer.selectedValue != undefined) {
              queries[`${field.name}_analyzer`] = field.analyzer.selectedValue;
            }
            if (field.boolean.selectedValue != undefined) {
              queries[`${field.name}_bool`] = field.boolean.selectedValue;
            }
            break;
          case AdvancedSearchFieldType.Range:
            if (field.gte !== undefined && !Number.isNaN(Number(field.gte as string))) {
              queries[`${field.name}_gte`] = field.gte;
            }
            if (field.lte !== undefined && !Number.isNaN(Number(field.lte as string))) {
              queries[`${field.name}_lte`] = field.lte;
            }
            break;
          case AdvancedSearchFieldType.Duration:
            if (field.gte !== undefined) {
              if (!Number.isNaN(Number(field.gte as string))) {
                queries[`${field.name}_gte`] = field.gte;
              } else {
                const gte = durationToSecond(field.gte as string);
                if (!Number.isNaN(gte)) {
                  queries[`${field.name}_gte`] = gte;
                }
              }
            }
            if (field.lte !== undefined) {
              if (!Number.isNaN(Number(field.lte as string))) {
                queries[`${field.name}_lte`] = field.lte;
              } else {
                const lte = durationToSecond(field.lte as string);
                if (!Number.isNaN(lte)) {
                  queries[`${field.name}_lte`] = lte;
                }
              }
            }
            break;
        }
      }

      let k = 1;
      for (let i = 0; i < labels.chips.length; i++) {
        const chip = labels.chips[i];
        if (chip.title !== undefined) {
          queries[`label_${k}`] = chip.title;
          k++;
        }
      }

      k = 1;
      for (let tagField in sourceState.data.tags) {
        const chips = privateState.tagFields[tagField].chips;
        for (const chip of chips) {
          queries[`tag_field_${k}`] = tagField;
          queries[`tag_value_${k}`] = chip.title;
          k++;
        }
      }

      const queriesArray = [];
      for (const key in queries) {
        queriesArray.push(`${key}=${queries[key]}`);
      }

      const queriesStr = queriesArray.join("&");
      const url = `/${props.state.category}/advanced-search?${queriesStr}`;

      router.push(url);
      advancedSearch.value.close();
    }

    function reset() {}

    function open() {
      advancedSearch.value.open();
    }

    function tokenToOption(token: { id: number; name: string }) {
      return { title: token.name, value: token.id };
    }

    return {
      advancedSearch,
      AdvancedSearchFieldType,
      categories,
      getStartWithTagFields,
      getTagTokenStartWith,
      labels,
      onGetCategories,
      onGetCategoriesToOptions,
      onGetTip,
      onGetUploader,
      onGetUploaderToOptions,
      onMouseoverOption,
      open,
      Origin,
      privateState,
      reset,
      search,
      SelectDropdownMode,
      sourceState,
      state,
      tagFields,
      tokenToOption,
      toTitle,
      uploader,
    };
  },
};
</script>
