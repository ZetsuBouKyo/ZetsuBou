<script setup lang="ts">
import { watch } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownMode, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";
import { CrudTableState, Header, Search } from "@/elements/Table/CrudTable/interface";

import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import CrudTable from "@/elements/Table/CrudTable/index.vue";

import { getTagAttributes } from "@/api/v1/tag/attribute";
import {
  TagInterpretation,
  deleteTag,
  getTagInterpretation,
  postTag,
  putTag,
  searchForTagAttributes,
} from "@/api/v1/tag/tag";
import { getTagTokenStartsWith, getTagTokenTotal, getTagTokens } from "@/api/v1/tag/token";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";

import { toTitle } from "@/utils/str";
import { onGetTip, onMouseoverOption } from "@/utils/tag";

interface Row {
  id?: number;
  name: string;
  representative_id: number;
  synonym_ids: Array<number>;
  category_ids: Array<number>;
  attributes: { [key: number]: string };
}

const table = initCrudTableState() as CrudTableState<Row>;
const headers: Array<Header> = [
  { title: "Id", key: "id" },
  { title: "Name", key: "name" },
];

const onCrudCreate = postTag;
const onCrudGet = getTagTokens;
const onCrudGetTotal = getTagTokenTotal;
const onCrudUpdate = putTag;
const onCrudDelete = deleteTag;

const onGetTokens = getTagTokenStartsWith;
function onGetTokensToOptions(data: { name: string | number; id: number }) {
  return { title: data.name, value: data.id };
}

const search: Search = {
  name: {
    title: "name",
    onSearch: getTagTokenStartsWith,
    onSearchToOptions: onGetTokensToOptions,
    onSearchGetTip: onGetTip,
    onSearchMouseoverOption: onMouseoverOption,
  },
  attribute: {
    title: "Attribute",
    onSearch: searchForTagAttributes,
    onSearchToOptions: onGetTokensToOptions,
    onSearchGetTip: onGetTip,
    onSearchMouseoverOption: onMouseoverOption,
  },
};

const representative = initSelectDropdownState() as SelectDropdownState;
watch(
  () => representative.selectedValue,
  () => {
    table.row.representative_id = representative.selectedValue as number;
  },
);
watch(
  () => representative.title,
  () => {
    if (!representative.title) {
      representative.selectedValue = undefined;
    }
  },
);

const synonyms = initSelectDropdownState() as SelectDropdownState;
watch(
  () => synonyms.chips.length,
  () => {
    table.row.synonym_ids = [];
    for (let i = 0; i < synonyms.chips.length; i++) {
      const chip = synonyms.chips[i];
      table.row.synonym_ids.push(chip.value as number);
    }
  },
);

const categories = initSelectDropdownState() as SelectDropdownState;
watch(
  () => categories.chips.length,
  () => {
    table.row.category_ids = [];
    for (let i = 0; i < categories.chips.length; i++) {
      const chip = categories.chips[i];
      table.row.category_ids.push(chip.value as number);
    }
  },
);

const attributes = initSelectDropdownState() as SelectDropdownState;

const onGetAttributes = getTagAttributes;
function onGetAttributesToOptions(data: { name: string | number; id: number }) {
  return { title: data.name, value: data.id };
}

function getAttributeTitleByID(id: number | string) {
  for (let i = 0; i < attributes.chips.length; i++) {
    const chip = attributes.chips[i];
    if (chip.value.toString() === id.toString()) {
      return toTitle(chip.title);
    }
  }
}

watch(
  () => attributes.chips.length,
  () => {
    if (table.row.attributes === undefined) {
      table.row.attributes = {};
    }
    const chipValues = [];
    for (let i = 0; i < attributes.chips.length; i++) {
      const chip = attributes.chips[i];
      if (table.row.attributes[chip.value] === undefined) {
        table.row.attributes[chip.value] = undefined;
      }
      chipValues.push(chip.value.toString());
    }
    for (let key in table.row.attributes) {
      if (!chipValues.includes(key.toString())) {
        delete table.row.attributes[key];
      }
    }
  },
);

function onCloseEditor() {
  table.row = {
    name: undefined,
    synonym_ids: [],
    category_ids: [],
    representative_id: undefined,
    attributes: {},
  };
  synonyms.reset();
  categories.reset();
  attributes.reset();
}

watch(
  () => {
    if (table.row) {
      return table.row.id;
    }
    return false;
  },
  () => {
    const tagID = table.row.id;
    if (tagID === undefined) {
      return;
    }
    getTagInterpretation(tagID).then((response) => {
      const tag = response.data as TagInterpretation;
      if (tag) {
        if (tag.representative) {
          representative.title = tag.representative.name;
          representative.selectedValue = tag.representative.id;
        }

        if (tag.attributes) {
          const attributeChips = [];
          for (let i = 0; i < tag.attributes.length; i++) {
            const attr = tag.attributes[i];
            attributeChips.push({ title: attr.name, value: attr.id });

            if (table.row.attributes === undefined) {
              table.row.attributes = {};
            }
            const attrID = attr.id.toString() as string;
            table.row.attributes[attrID] = attr.value;
          }
          attributes.chips = attributeChips;
        }
        // console.log(table);

        if (tag.categories) {
          const categoryChips = [];
          for (let i = 0; i < tag.categories.length; i++) {
            const category = tag.categories[i];
            categoryChips.push({ title: category.name, value: category.id });
          }
          categories.chips = categoryChips;
        }

        if (tag.synonyms) {
          const synonymChips = [];
          for (let i = 0; i < tag.synonyms.length; i++) {
            const synonym = tag.synonyms[i];
            synonymChips.push({ title: synonym.name, value: synonym.id });
          }
          synonyms.chips = synonymChips;
        }
      }
    });
  },
);
</script>

<template>
  <div class="views-setting-container">
    <crud-table
      class="w-full"
      :state="table"
      :editor-title="'Tag'"
      :headers="headers"
      :search="search"
      :colspan="'3'"
      :on-crud-create="onCrudCreate"
      :on-crud-get="onCrudGet"
      :on-crud-get-total="onCrudGetTotal"
      :on-crud-update="onCrudUpdate"
      :on-crud-delete="onCrudDelete"
      :on-close-editor="onCloseEditor"
      :delete-confirm-message="'Are you sure you want to permanently delete this row? This might destroy the database.'">
      <template v-slot:editor>
        <div class="modal-row h-10">
          <span class="w-32 mr-4">Name:</span>
          <input class="w-1/2 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
        </div>
        <div class="modal-row h-10">
          <span class="w-32 mr-4">Representative:</span>
          <select-dropdown
            class="flex-1"
            :options-width-class="'w-64'"
            :origin="Origin.BottomLeft"
            :state="representative"
            :on-get="onGetTokens"
            :on-get-to-options="onGetTokensToOptions"
            :on-get-tip="onGetTip"
            :on-mouseover-option="onMouseoverOption"
            :mode="SelectDropdownMode.Input" />
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Synonyms:</span>
          <select-dropdown
            class="flex-1"
            :options-width-class="'w-64'"
            :origin="Origin.BottomLeft"
            :state="synonyms"
            :enable-input-chips-enter-event="false"
            :on-get="onGetTokens"
            :on-get-to-options="onGetTokensToOptions"
            :on-get-tip="onGetTip"
            :on-mouseover-option="onMouseoverOption"
            :mode="SelectDropdownMode.InputChips" />
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Categories:</span>
          <select-dropdown
            class="flex-1"
            :options-width-class="'w-96'"
            :origin="Origin.BottomLeft"
            :state="categories"
            :enable-input-chips-enter-event="false"
            :on-get="onGetTokens"
            :on-get-to-options="onGetTokensToOptions"
            :on-get-tip="onGetTip"
            :on-mouseover-option="onMouseoverOption"
            :mode="SelectDropdownMode.InputChips" />
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Attributes:</span>
          <select-dropdown
            class="flex-1"
            :options-width-class="'w-96'"
            :origin="Origin.BottomLeft"
            :state="attributes"
            :enable-input-chips-enter-event="false"
            :on-get="onGetAttributes"
            :on-get-to-options="onGetAttributesToOptions"
            :mode="SelectDropdownMode.InputChips" />
        </div>
        <div class="modal-row" v-for="(_, chipID) in table.row.attributes" :key="chipID">
          <span class="w-32 mr-4">{{ getAttributeTitleByID(chipID) }}:</span>
          <textarea class="modal-textarea flex-1 h-40" v-model="table.row.attributes[chipID]" />
        </div>
      </template>
    </crud-table>
  </div>
</template>
