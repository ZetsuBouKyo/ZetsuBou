<template>
  <div class="flex flex-col w-full mx-auto my-4 bg-gray-900 rounded-lg shadow-black">
    <confirm-modal
      ref="confirm"
      :title="'Warning'"
      :message="
        deleteConfirmMessage === undefined
          ? 'Are you sure you want to permanently delete this row?'
          : deleteConfirmMessage
      "
      :on-confirm="onConfirm"
    />
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
        :mode="SelectDropdownMode.Input"
      />
    </div>
    <modal
      ref="editor"
      :title="editorTitle"
      :is-scrollable="isEditorScrollable"
      :on-open="onOpenEditor"
      :on-close="onCloseEditor"
      :class="editorClass"
    >
      <slot name="editor"></slot>
      <div class="modal-row">
        <button class="flex ml-auto btn btn-primary" @click="editor.close">Cancel</button>
        <button class="flex ml-2 btn btn-primary" @click="state.editor.handler">Save</button>
      </div>
    </modal>
    <div class="overflow-x-auto scrollbar-gray-900-2 w-full" :class="isEmpty(search) ? 'rounded-lg' : ''">
      <table class="table-auto w-full text-left whitespace-no-wrap" v-if="state.sheet">
        <thead>
          <tr class="table-head">
            <th class="table-data" v-for="(h, i) in state.sheet.headers" :key="i" :class="i === 0 ? 'w-20' : ''">
              {{ h.title }}
            </th>
            <th class="table-data">Operation</th>
          </tr>
        </thead>
        <tbody>
          <tr class="table-row" v-for="(row, i) in state.sheet.rows" :key="i">
            <td class="table-data" v-for="(header, j) in state.sheet.headers" :key="j">
              {{ header.handler ? header.handler(row[header.key]) : row[header.key] }}
            </td>
            <td class="table-data flex flex-row items-center">
              <slot name="buttons" :row="row"></slot>
              <crud-table-button :text="'Edit'" :color="ButtonColorEnum.Primary" :row="row" :onClick="update">
                <template v-slot:icon><icon-mdi-file-edit-outline /></template>
              </crud-table-button>
              <crud-table-button :text="'Delete'" :color="ButtonColorEnum.Danger" :row="row" :onClick="confirmRemove">
                <template v-slot:icon><icon-mdi-trash-can-outline /></template>
              </crud-table-button>
            </td>
          </tr>
          <tr :class="state.pagination ? 'table-row' : ''">
            <td class="table-data" :colspan="colspan">
              <ripple-button class="btn w-full btn-primary" @click="create">+</ripple-button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <pagination-base class="ml-auto mr-4" v-if="state.pagination" :pagination="state.pagination" />
  </div>
</template>

<script lang="ts">
import axios, { AxiosResponse } from "axios";
import { defineComponent, PropType, reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { isEmpty } from "@/utils/obj";

import { ButtonColorEnum } from "@/elements/Button/button.ts";
import ConfirmModal from "@/elements/Modal/ConfirmModal.vue";
import CrudTableButton from "@/elements/Table/CrudTable/CrudTableButton.vue";
import Modal from "@/elements/Modal/Modal.vue";
import PaginationBase from "@/elements/Pagination/index.vue";
import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown, {
  SelectDropdownOption,
  SelectDropdownState,
  SelectDropdownMode,
  Origin,
  OnGetToOptions,
  OnGetTip,
  OnMouseoverOption,
  reset,
} from "@/elements/Dropdown/SelectDropdown.vue";

import { getPagination } from "@/elements/Pagination/pagination";

import { Pagination } from "@/elements/Pagination/interface";

export interface Header {
  title: string;
  key: string;
  handler?: (value: string | number) => string | number;
}

export interface Row {
  id?: number;
  [key: string]: any;
}

export interface GetParam {
  page: number;
  size: number;
  [key: string]: any;
}

export interface Sheet {
  headers: Array<Header>;
  rows: Array<Row>;
}

export interface CrudTableState<Row> {
  sheet: Sheet;
  pagination: Pagination;
  row: Row;
  cache: Row;
  editor: {
    handler: () => void;
    title: string;
  };
  [key: string]: any;
}

export interface Editor {
  popout: boolean;
}

export interface OnSearch {
  (params: GetParam): Promise<AxiosResponse<Array<Row>>>;
}

export interface SearchOption {
  title: string;
  onSearch: OnSearch;
  onSearchToOptions: OnGetToOptions;
  onSearchGetTip?: OnGetTip;
  onSearchMouseoverOption?: OnMouseoverOption;
}

export interface Search {
  [key: string]: SearchOption;
}

export interface OnCrudCreate {
  (row: Row): Promise<AxiosResponse<Row>>;
}

export interface OnCrudGet {
  (params: GetParam): Promise<AxiosResponse<Array<Row>>>;
}

export interface OnCrudGetTotal {
  (): Promise<AxiosResponse<number>>;
}

export interface OnCrudUpdate {
  (row: Row): Promise<AxiosResponse<any>>;
}

export interface OnCrudDelete {
  (id: number): Promise<AxiosResponse<Array<any>>>;
}

export interface OnOpenEditor {
  (): void;
}

export interface OnCloseEditor {
  (): void;
}

function initState(row?: Row): CrudTableState<Row> {
  return reactive<CrudTableState<Row>>({
    sheet: undefined,
    pagination: undefined,
    row: row,
    cache: undefined,
    editor: {
      handler: undefined,
      title: undefined,
    },
  });
}

export default defineComponent({
  components: { ConfirmModal, CrudTableButton, Modal, PaginationBase, RippleButton, SelectDropdown },
  initState,
  props: {
    state: {
      type: Object as PropType<CrudTableState<Row>>,
      default: initState(),
    },
    colspan: {
      type: Object as PropType<string>,
      default: undefined,
    },
    headers: {
      type: Object as PropType<Array<Header>>,
      default: undefined,
    },
    search: {
      type: Object as PropType<Search>,
      default: {},
    },
    editorTitle: {
      type: Object as PropType<string>,
      default: "Editor",
    },
    editorClass: {
      type: Object as PropType<string>,
      default: "w-1/2 top-1/4 left-1/4",
    },
    isEditorScrollable: {
      type: Object as PropType<boolean>,
      default: false,
    },
    deleteConfirmMessage: {
      type: Object as PropType<string>,
      default: undefined,
    },
    onCrudCreate: {
      type: Object as PropType<OnCrudCreate>,
      default: undefined,
    },
    onCrudGet: {
      type: Object as PropType<OnCrudGet>,
      default: undefined,
    },
    onCrudGetTotal: {
      type: Object as PropType<OnCrudGetTotal>,
      default: undefined,
    },
    onCrudUpdate: {
      type: Object as PropType<OnCrudUpdate>,
      default: undefined,
    },
    onCrudDelete: {
      type: Object as PropType<OnCrudDelete>,
      default: undefined,
    },
    onOpenEditor: {
      type: Object as PropType<OnOpenEditor>,
      default: undefined,
    },
    onCloseEditor: {
      type: Object as PropType<OnCloseEditor>,
      default: undefined,
    },
  },
  setup(props) {
    const state = props.state;
    const headers = props.headers;
    const editor = ref();

    const route = useRoute();
    const params: GetParam = {
      page: route.query.page ? parseInt(route.query.page as string) : 1,
      size: route.query.size ? parseInt(route.query.size as string) : 20,
    };

    const searchFieldState = SelectDropdown.initState() as SelectDropdownState;
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

    const searchValueState = SelectDropdown.initState() as SelectDropdownState;
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
      if (props.onCrudGet !== undefined && props.onCrudGetTotal !== undefined) {
        axios.all<any>([props.onCrudGetTotal(), props.onCrudGet(params)]).then(
          axios.spread((response1, response2) => {
            const totalItems = response1.data;
            const rows = response2.data;
            state.pagination = getPagination(route.path, totalItems, params);
            state.sheet = { headers: headers, rows: rows };
          }),
        );
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
      state.editor.handler = () => {
        props.onCrudCreate(state.row).then((response: any) => {
          if (response.status === 200) {
            editor.value.close();
            window.location.reload();
          }
        });
      };
      editor.value.open();
    }

    function update(row: Row) {
      state.row = row;
      state.editor.handler = () => {
        props.onCrudUpdate(state.row).then((response: any) => {
          if (response.status !== 200) {
          } else {
            editor.value.close();
            window.location.reload();
          }
        });
      };
      editor.value.open();
    }

    function deleteById(id: any) {
      props.onCrudDelete(id).then((response: any) => {
        if (response.status === 200) {
        }
      });
    }

    const confirm = ref();

    function onConfirm() {
      deleteById(state.row.id);
      state.row = undefined;
      window.location.reload();
    }

    function confirmRemove(row: any) {
      state.row = row;
      confirm.value.open();
    }

    return {
      ButtonColorEnum,
      SelectDropdownMode,
      Origin,
      isEmpty,
      state,
      searchFieldState,
      searchValueState,
      onSearch,
      onSearchToOptions,
      onSearchGetTip,
      onSearchMouseoverOption,
      editor,
      onOpenEditor,
      onCloseEditor,
      confirm,
      onConfirm,
      confirmRemove,
      create,
      update,
    };
  },
});
</script>
