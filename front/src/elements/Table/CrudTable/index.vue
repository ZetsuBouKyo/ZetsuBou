<script setup lang="ts">
import axios from "axios";
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

import { ButtonColorEnum } from "@/elements/Button/button.interface";
import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import {
  SelectDropdownMode,
  SelectDropdownOption,
  SelectDropdownState,
} from "@/elements/Dropdown/SelectDropdown.interface";
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

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import ConfirmModal from "@/elements/Modal/ConfirmModal.vue";
import Modal from "@/elements/Modal/Modal.vue";
import PaginationBase from "@/elements/Pagination/index.vue";
import CrudTableButton from "@/elements/Table/CrudTable/CrudTableButton.vue";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { messageState } from "@/state/message";
import { routeState } from "@/state/route";

import { getPagination } from "@/elements/Pagination/pagination";
import { isEmpty } from "@/utils/obj";
import { initCrudTableState } from "./CrudTable";

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
  onCrudCreate: OnCrudCreate;
  onCrudGet: OnCrudGet;
  onCrudGetTotal: OnCrudGetTotal;
  onCrudUpdate: OnCrudUpdate;
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

const searchFieldState = initSelectDropdownState() as SelectDropdownState;
if (!isEmpty(props.search)) {
  const keys = Object.keys(props.search);
  const key = keys[0];
  searchFieldState.title = props.search[key].title;
}
for (const title in props.search) {
  searchFieldState.options.push({ title: title, value: title });
}
function onSearch(params: any) {
  return props.search[searchFieldState.title].onSearch(params);
}
function onSearchToOptions(data: any) {
  return props.search[searchFieldState.title].onSearchToOptions(data);
}

function onSearchGetTip(opt: SelectDropdownOption) {
  return props.search[searchFieldState.title].onSearchGetTip(opt);
}

function onSearchMouseoverOption(event, opt: SelectDropdownOption) {
  return props.search[searchFieldState.title].onSearchMouseoverOption(event, opt);
}

const searchValueState = initSelectDropdownState() as SelectDropdownState;
watch(
  () => searchValueState.options.length,
  () => {
    if (searchValueState.title === undefined) {
      load();
      return;
    }
    if (typeof searchValueState.title === "string" && searchValueState.title.length > 0) {
      state.pagination = undefined;
      state.sheet.rows = [];
      for (const opt of searchValueState.options) {
        state.sheet.rows.push(opt.raw);
      }
    } else {
      load();
    }
  },
);

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

function create() {
  state.row = {};
  state.editor.type = EditorTypeEnum.Create;
  state.editor.handler = () => {
    props.onCrudCreate(state.row).then((response: any) => {
      if (response.status === 200) {
        editor.value.close();
        load();
        messageState.push("Created");
      }
    });
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
    props.onCrudUpdate(state.row).then((response: any) => {
      if (response.status !== 200) {
      } else {
        editor.value.close();
        load();
        messageState.push("Updated");
      }
    });
  };
  editor.value.open();
}

function deleteById(id: any) {
  props.onCrudDelete(id).then((response: any) => {
    if (response.status !== 200) {
    } else {
      load();
      messageState.push("Deleted");
    }
  });
}

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
    <select-dropdown class="w-64 h-10 mr-4" :options-width-class="'w-64'" :state="searchFieldState" />
    <select-dropdown
      class="flex-1"
      :options-width-class="'w-64'"
      :origin="Origin.BottomLeft"
      :state="searchValueState"
      :on-get="onSearch"
      :on-get-to-options="onSearchToOptions"
      :on-get-tip="onSearchGetTip"
      :on-mouseover-option="onSearchMouseoverOption"
      :mode="SelectDropdownMode.Input" />
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
