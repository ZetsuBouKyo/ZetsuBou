<script setup lang="ts">
import { ref } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownOption } from "@/elements/Dropdown/SelectDropdown.interface";
import {
  CrudTableState,
  Header,
  OnCrudCreate,
  OnCrudDelete,
  OnCrudGet,
  OnCrudGetTotal,
  OnCrudUpdate,
} from "@/elements/Table/CrudTable/interface";
import { Row } from "./ElasticQueryTable.interface";

import RippleButtonSelectDropdown from "@/elements/Dropdown/RippleButtonSelectDropdown.vue";
import CrudTable from "@/elements/Table/CrudTable/index.vue";

import { getQueryExample } from "@/api/v1/elasticsearch";

import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";

import { getDatetime } from "@/utils/datetime";

interface Props {
  editorTitle: string;
  onCrudCreate: OnCrudCreate;
  onCrudGet: OnCrudGet;
  onCrudGetTotal: OnCrudGetTotal;
  onCrudUpdate: OnCrudUpdate;
  onCrudDelete: OnCrudDelete;
}
const props = withDefaults(defineProps<Props>(), {
  editorTitle: undefined,
  onCrudCreate: undefined,
  onCrudGet: undefined,
  onCrudGetTotal: undefined,
  onCrudUpdate: undefined,
  onCrudDelete: undefined,
});

const table = initCrudTableState() as CrudTableState<Row>;
const headers: Array<Header> = [
  { title: "Id", key: "id" },
  { title: "Name", key: "name" },
  { title: "Created", key: "created", handler: getDatetime },
  { title: "Modified", key: "modified", handler: getDatetime },
];

const example = ref();
const exampleTitle = ref("");
const exampleSelectedValue = ref(undefined);
const exampleOptions = ref([]);

function onSelect(opt: SelectDropdownOption) {
  table.row.query = JSON.stringify(opt.raw.value, null, 4);
}

function loadExample() {
  getQueryExample().then((response) => {
    const data = response.data;
    for (const q of data) {
      const option: SelectDropdownOption = {
        title: q.summary,
        value: q.summary,
        raw: q,
      };
      exampleOptions.value.push(option);
    }
  });
}
loadExample();

function onCloseEditor() {
  example.value.clear();
}
</script>

<template>
  <crud-table
    class="w-full"
    :state="table"
    :editor-title="editorTitle"
    :headers="headers"
    :colspan="'5'"
    :on-crud-create="onCrudCreate"
    :on-crud-get="onCrudGet"
    :on-crud-get-total="onCrudGetTotal"
    :on-crud-update="onCrudUpdate"
    :on-crud-delete="onCrudDelete"
    :on-close-editor="onCloseEditor">
    <template v-slot:editor>
      <div class="modal-row h-10">
        <span class="w-24 mr-4">Name:</span>
        <input class="flex-1 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
      </div>
      <div class="modal-row h-10">
        <span class="w-24 mr-4">Template:</span>
        <ripple-button-select-dropdown
          ref="example"
          class="h-10 w-64"
          v-model:title="exampleTitle"
          v-model:selected-value="exampleSelectedValue"
          v-model:options="exampleOptions"
          :options-width-class="'w-64'"
          :origin="Origin.BottomLeft"
          :on-select="onSelect" />
      </div>
      <div class="modal-row h-56">
        <textarea v-model="table.row.query" class="modal-textarea h-full" />
      </div>
    </template>
  </crud-table>
</template>
