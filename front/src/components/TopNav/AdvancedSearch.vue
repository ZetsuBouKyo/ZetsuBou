<template>
  <modal
    ref="advancedSearch"
    :title="'Advanced Search'"
    class="w-1/2 top-12 h-50v left-1/4"
    :is-scrollable="true"
    @keyup.enter="search"
  >
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
            :state="field.fuzziness"
          />
          <span class="w-16 mr-4">Analyzer:</span>
          <select-dropdown
            class="w-32 mr-4"
            :group="'search'"
            :options-width-class="'w-32'"
            :origin="Origin.BottomLeft"
            :state="field.analyzer"
          />
          <span class="w-16 mr-4">Boolean:</span>
          <select-dropdown
            class="w-28"
            :group="'search'"
            :options-width-class="'w-28'"
            :origin="Origin.BottomLeft"
            :state="field.boolean"
          />
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
      <input class="modal-input flex-1" type="text" :placeholder="category.value" v-model="category.value" />
    </div>
    <div class="modal-row" @keyup.enter.stop="">
      <span class="w-28 mr-4 text-white">Labels:</span>
      <select-dropdown
        class="flex-1"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="labels"
        :mode="SelectDropdownMode.InputChips"
      />
    </div>
    <div class="modal-row" @keyup.enter.stop="">
      <span class="w-28 mr-4 text-white">Tag Fields:</span>
      <select-dropdown
        class="flex-1"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="tagFields"
        :mode="SelectDropdownMode.InputChips"
      />
    </div>
    <div class="modal-row" v-for="(fieldState, field, index) in tags" :key="index" @keyup.enter.stop="">
      <span class="w-28 mx-4">{{ field }}:</span>
      <select-dropdown
        class="flex-1"
        :options-width-class="'w-64'"
        :origin="Origin.BottomLeft"
        :state="fieldState"
        :mode="SelectDropdownMode.InputChips"
      />
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

import { SearchAnalyzer } from "@/interface/search";

import { durationToSecond } from "@/utils/datetime";
import { toTitle } from "@/utils/str";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Modal from "@/elements/Modal/Modal.vue";

import SelectDropdown, {
  SelectDropdownMode,
  SelectDropdownState,
  Origin,
  reset,
} from "@/elements/Dropdown/SelectDropdown.vue";

import { messageState } from "@/state/message";

export enum AdvancedSearchFieldType {
  String,
  Range,
  Duration,
}

export interface AdvancedSearchField {
  name: string;
  type: AdvancedSearchFieldType;
  value?: string;
  fuzziness?: SelectDropdownState;
  analyzer?: SelectDropdownState;
  boolean?: SelectDropdownState;
  gte?: number | string;
  lte?: number | string;
}

export interface AdvancedSearchState {
  baseUrl: string;
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
          const searchAnalyzers = Object.values(SearchAnalyzer);
          for (let analyzer of searchAnalyzers) {
            field.analyzer.options.push({ title: toTitle(analyzer), value: analyzer });
          }

          field.boolean = SelectDropdown.initState() as SelectDropdownState;
          field.boolean.options = [
            { title: "Should", value: "should" },
            { title: "Must", value: "must" },
          ];
          break;
      }
    }

    const category = reactive({ value: undefined });

    const advancedSearch = ref();
    const labels = SelectDropdown.initState() as SelectDropdownState;

    const tags = reactive<{ [key: string]: SelectDropdownState }>({});
    const tagFields = SelectDropdown.initState() as SelectDropdownState;
    watch(
      () => tagFields.chips.length,
      () => {
        const chipTitles = [];
        for (const chip of tagFields.chips) {
          chipTitles.push(chip.title);
          if (tags[chip.title] === undefined) {
            tags[chip.title] = SelectDropdown.initState() as SelectDropdownState;
          }
        }
        for (const title in tags) {
          if (!chipTitles.includes(title)) {
            delete tags[title];
          }
        }
      },
    );

    function search() {
      const queries = {};

      if (category.value !== undefined) {
        queries["category"] = category.value;
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
      for (const field in tags) {
        const chips = tags[field].chips;
        for (const chip of chips) {
          queries[`tag_field_${k}`] = field;
          queries[`tag_value_${k}`] = chip.title;
          k++;
        }
      }

      const queriesArray = [];
      for (const key in queries) {
        queriesArray.push(`${key}=${queries[key]}`);
      }

      const queriesStr = queriesArray.join("&");
      const url = `${props.state.baseUrl}/advanced-search?${queriesStr}`;

      window.open(url, "_self");
    }

    function reset() {}

    function open() {
      advancedSearch.value.open();
    }

    return {
      ...props,
      AdvancedSearchFieldType,
      Origin,
      SelectDropdownMode,
      toTitle,
      advancedSearch,
      category,
      labels,
      tags,
      tagFields,
      search,
      reset,
      open,
    };
  },
};
</script>
