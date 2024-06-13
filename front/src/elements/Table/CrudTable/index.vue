<script setup lang="ts">
import axios from "axios";
import { ref, Ref, watch } from "vue";
import { useRoute } from "vue-router";

import { ButtonColorEnum } from "@/elements/Button/button.interface";
import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownOption, SelectDropdownGetParam } from "@/elements/Dropdown/SelectDropdown.interface";
import {
  CrudGetParam,
  CrudTableState,
  EditorTypeEnum,
  Header,
  OnCloseEditor,
  OnCrudCreate,
  OnCrudDelete,
  OnCrudGet,
  OnCrudGetTotal,
  OnCrudUpdate,
  OnOpenEditor,
  Row,
  Search,
} from "./interface";

import InputSelectDropdown from "@/elements/Dropdown/InputSelectDropdown.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";
import RippleButtonSelectDropdown from "@/elements/Dropdown/RippleButtonSelectDropdown.vue";
import ConfirmModal from "@/elements/Modal/ConfirmModal.vue";
import Modal from "@/elements/Modal/Modal.vue";
import PaginationBase from "@/elements/Pagination/index.vue";
import CrudTableButton from "@/elements/Table/CrudTable/CrudTableButton.vue";

import { messageState } from "@/state/message";
import { routeState } from "@/state/route";

import { getPagination } from "@/elements/Pagination/pagination";
import { isEmpty } from "@/utils/obj";
import { initCrudTableState } from "./CrudTable";

import { getFirstOptions, scroll, convertArrayDataToOptions } from "@/elements/Dropdown/SelectDropdown";

interface Props {
  state: CrudTableState<Row>;
  colspan: string;
  headers: Array<Header>;
  search: Search;
  editorTitle: string;
  editorClass: string;
  isEditorScrollable: boolean;
  isAddible: boolean;
  isRowEditable: boolean;
  isRowDeletable: boolean;
  areRowsCustom: boolean;
  deleteConfirmMessage: string;
  onCrudCreate?: OnCrudCreate;
  onCrudGet: OnCrudGet;
  onCrudGetTotal: OnCrudGetTotal;
  onCrudUpdate?: OnCrudUpdate;
  onCrudDelete: OnCrudDelete;
  onOpenEditor: OnOpenEditor;
  onCloseEditor: OnCloseEditor;
}
const props = withDefaults(defineProps<Props>(), {
  state: () => initCrudTableState(),
  colspan: undefined,
  headers: undefined,
  search: () => <Search>{},
  editorTitle: "Editor",
  editorClass: "w-1/2 top-1/4 left-1/4",
  isEditorScrollable: false,
  isAddible: true,
  isRowEditable: true,
  isRowDeletable: true,
  areRowsCustom: false,
  deleteConfirmMessage: undefined,
  onCrudCreate: undefined,
  onCrudGet: undefined,
  onCrudGetTotal: undefined,
  onCrudUpdate: undefined,
  onCrudDelete: undefined,
  onOpenEditor: undefined,
  onCloseEditor: undefined,
});

const state = props.state;
const headers = props.headers;
const editor = ref();

const route = useRoute();

// Search field
const searchFieldTitle = ref("");
const searchFieldSelectedValue = ref(undefined);
const searchFieldOptions = ref([]);

// Load search fields
if (!isEmpty(props.search)) {
  const keys = Object.keys(props.search);
  const key = keys[0];
  searchFieldTitle.value = props.search[key].title;
}
for (const title in props.search) {
  searchFieldOptions.value.push({ title: title, value: title });
}

// Queries for search fields
function onSearch(params: any) {
  return props.search[searchFieldTitle.value].onSearch(params);
}
function onSearchToOptions(data: any) {
  return props.search[searchFieldTitle.value].onSearchToOptions(data);
}

function onSearchGetTip(opt: SelectDropdownOption) {
  return props.search[searchFieldTitle.value].onSearchGetTip(opt);
}

function onSearchMouseoverOption(event, opt: SelectDropdownOption) {
  return props.search[searchFieldTitle.value].onSearchMouseoverOption(event, opt);
}

// Search value
interface SearchValueT {}
const searchValueTitle = ref("");
const searchValueSelectedValue = ref(undefined);
const searchValueOptions = ref([]);
const searchValueScrollEnd = ref<boolean>(false);

const searchValueParams = ref<SelectDropdownGetParam>({ page: 1, size: 20, s: "" });
const searchValueLock = ref<boolean>(false);

function convertSearchValue(data: Array<any>, options: Ref<Array<SelectDropdownOption>>) {
  convertArrayDataToOptions<SearchValueT>(onSearchToOptions, data, options);
}
function getSearchValue(params: SelectDropdownGetParam) {
  return onSearch(params);
}
function inputSearchValue(s: string) {
  searchValueParams.value.s = s;
  openSearchValue();
}
function openSearchValue() {
  getFirstOptions(
    getSearchValue,
    convertSearchValue,
    searchValueParams,
    searchValueOptions,
    searchValueLock,
    searchValueScrollEnd,
  );
}
function scrollSearchValue(event: any) {
  scroll(
    event,
    getSearchValue,
    convertSearchValue,
    searchValueParams,
    searchValueOptions,
    searchValueLock,
    searchValueScrollEnd,
  );
}
function selectSearchValue(opt: SelectDropdownOption) {
  if (opt.value === undefined) {
    load();
    return;
  }
  if (typeof opt.title === "string" && opt.title.length > 0) {
    state.pagination = undefined;
    state.sheet.rows = [];
    state.sheet.rows.push(opt.raw);
  } else {
    load();
  }
}
watch(
  () => {
    return searchValueOptions.value.length;
  },
  () => {
    if (searchValueTitle.value) {
      state.pagination = undefined;
      state.sheet.rows = [];

      for (const opt of searchValueOptions.value) {
        state.sheet.rows.push(opt.raw);
      }
    } else {
      load();
    }
  },
);

// Load data from queries.
function load() {
  const params: CrudGetParam = {
    page: route.query.page ? parseInt(route.query.page as string) : 1,
    size: route.query.size ? parseInt(route.query.size as string) : 20,
  };

  if (props.onCrudGet !== undefined && props.onCrudGetTotal !== undefined) {
    axios.all<any>([props.onCrudGetTotal(), props.onCrudGet(params)]).then(
      axios.spread((response1, response2) => {
        const totalItems = response1.data;
        const rows = response2.data;
        state.pagination = getPagination(route.path, totalItems, params);
        state.sheet = { headers: headers, rows: rows };
      }),
    );
  } else {
    state.sheet = { headers: headers, rows: [] };
  }
}
load();

// Editor
function onOpenEditor() {
  if (state.row) {
    state.cache = JSON.parse(JSON.stringify(state.row));
  }
  if (props.onOpenEditor !== undefined) {
    props.onOpenEditor();
  }
}

function onCloseEditor() {
  if (state.cache) {
    for (let key in state.cache) {
      state.row[key] = state.cache[key];
    }
  }
  if (props.onCloseEditor !== undefined) {
    props.onCloseEditor();
  }
}

// CRUD
function create() {
  state.row = {};
  state.editor.type = EditorTypeEnum.Create;
  state.editor.handler = () => {
    try {
      props.onCrudCreate(state.row).then((response: any) => {
        if (response.status === 200) {
          editor.value.close();
          load();
          messageState.push("Created");
        }
      });
    } catch (error) {
      if (!(error instanceof TypeError)) {
        throw error;
      }
    }
  };
  editor.value.open();
}

function update(row: Row) {
  if (!props.isRowEditable) {
    return;
  }
  state.row = row;
  state.editor.type = EditorTypeEnum.Update;
  state.editor.handler = () => {
    try {
      props.onCrudUpdate(state.row).then((response: any) => {
        if (response.status !== 200) {
        } else {
          editor.value.close();
          load();
          messageState.push("Updated");
        }
      });
    } catch (error) {
      if (!(error instanceof TypeError)) {
        throw error;
      }
    }
  };
  editor.value.open();
}

function deleteById(id: any) {
  try {
    props.onCrudDelete(id).then((response: any) => {
      if (response.status !== 200) {
      } else {
        load();
        messageState.push("Deleted");
      }
    });
  } catch (error) {
    if (!(error instanceof TypeError)) {
      throw error;
    }
  }
}

// Confirm box
const confirm = ref();

function onConfirm() {
  deleteById(state.row.id);
  state.row = undefined;
}

function confirmRemove(row: any) {
  if (!props.isRowDeletable) {
    return;
  }
  state.row = row;
  confirm.value.open();
}

routeState.setRoute(route);
routeState.setLoadFunction(load);
</script>

<template>
  <confirm-modal
    ref="confirm"
    :title="'Warning'"
    :message="
      deleteConfirmMessage === undefined
        ? 'Are you sure you want to permanently delete this row?'
        : deleteConfirmMessage
    "
    :on-confirm="onConfirm" />
  <div class="flex flex-row mx-4 my-2 items-center" v-if="!isEmpty(search)">
    <ripple-button-select-dropdown
      class="w-64 h-10 mr-4"
      v-model:title="searchFieldTitle"
      v-model:selected-value="searchFieldSelectedValue"
      v-model:options="searchFieldOptions"
      :options-width-class="'w-64'" />
    <input-select-dropdown
      class="flex-1"
      v-model:title="searchValueTitle"
      v-model:selected-value="searchValueSelectedValue"
      v-model:options="searchValueOptions"
      v-model:scroll-end="searchValueScrollEnd"
      :is-auto-complete="true"
      :options-width-class="'w-64'"
      :origin="Origin.BottomLeft"
      :on-get-tip="onSearchGetTip"
      :on-input="inputSearchValue"
      :on-open="openSearchValue"
      :on-scroll="scrollSearchValue"
      :on-select="selectSearchValue"
      :on-mouseover-option="onSearchMouseoverOption" />
  </div>
  <modal
    ref="editor"
    :title="editorTitle"
    :is-scrollable="isEditorScrollable"
    :on-open="onOpenEditor"
    :on-close="onCloseEditor"
    :class="editorClass">
    <slot name="editor"></slot>
    <slot name="editor-create" v-if="state.editor.type === EditorTypeEnum.Create"></slot>
    <slot name="editor-update" v-else-if="state.editor.type === EditorTypeEnum.Update"></slot>
    <div class="modal-row-reverse h-10">
      <button class="flex ml-2 btn btn-primary" @click="state.editor.handler">Save</button>
      <button class="flex ml-2 btn btn-primary" @click="editor.close">Cancel</button>
      <slot name="editor-buttons"></slot>
    </div>
  </modal>
  <div class="table-container" :class="isEmpty(search) ? 'rounded-lg' : ''">
    <table class="table-container" v-if="state.sheet">
      <thead>
        <tr class="table-head">
          <th class="table-row-data" v-for="(h, i) in state.sheet.headers" :key="i" :class="i === 0 ? 'w-20' : ''">
            {{ h.title }}
          </th>
          <th class="table-row-data">Operation</th>
        </tr>
      </thead>
      <tbody>
        <slot name="rows"></slot>
        <tr class="table-row" v-for="(row, i) in state.sheet.rows" :key="i">
          <td class="table-row-data" v-for="(header, j) in state.sheet.headers" :key="j">
            {{ header.handler ? header.handler(row[header.key]) : row[header.key] }}
          </td>
          <td class="table-row-buttons">
            <slot name="buttons" :row="row"></slot>
            <crud-table-button
              :text="'Edit'"
              :color="ButtonColorEnum.Primary"
              :row="row"
              :onClick="update"
              v-if="isRowEditable">
              <template v-slot:icon><icon-mdi-file-edit-outline /></template>
            </crud-table-button>
            <crud-table-button
              :text="'Delete'"
              :color="ButtonColorEnum.Danger"
              :row="row"
              :onClick="confirmRemove"
              v-if="isRowDeletable">
              <template v-slot:icon><icon-mdi-trash-can-outline /></template>
            </crud-table-button>
          </td>
        </tr>
        <tr :class="state.pagination ? 'table-row' : ''" v-if="isAddible">
          <td class="table-row-data" :colspan="colspan">
            <ripple-button class="btn w-full btn-primary" @click="create">+</ripple-button>
          </td>
        </tr>
      </tbody>
    </table>
    <pagination-base
      class="ml-auto mr-4"
      v-if="state.pagination"
      :pagination="state.pagination"
      :key="state.pagination.current" />
  </div>
</template>
