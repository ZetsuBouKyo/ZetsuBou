<script setup lang="ts">
import { reactive, watch } from "vue";

import { CrudTableState, Header } from "@/elements/Table/CrudTable/interface";

import CrudTable from "@/elements/Table/CrudTable/index.vue";

import { deleteGroup, getGroup, getGroupTotal, postGroup, putGroup } from "@/api/v1/group";

import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";

interface Scope {
  group_id: number;
  id: number;
  name?: string;
}

interface Row {
  id?: number;
  name: string;
  scopes: Array<Scope>;
}

const table = initCrudTableState() as CrudTableState<Row>;

const prefix = reactive({
  options: [],
});

watch(
  () => table.row,
  () => {
    // const bucketName = bucketsDropdown.selectedValue as string;
    // const prefixName = table.row.prefix as string;
    // if (bucketName === undefined || prefixName === undefined) {
    //   return;
    // }
    // if (prefixName.slice(-1) === "/") {
    //   getPrefixAutoComplete(bucketName, prefixName);
    // }
  },
);

function load() {
  // getMinioStorageCategories().then((response) => {
  //   const data = response.data;
  //   if (data) {
  //     for (let key in data) {
  //       categoriesDropdown.options.push({ title: key, value: data[key] });
  //     }
  //   }
  // });
}

const headers: Array<Header> = [
  { title: "Id", key: "id" },
  { title: "Name", key: "name" },
];

const onCrudCreate = postGroup;
const onCrudGet = getGroup;
const onCrudGetTotal = getGroupTotal;
const onCrudUpdate = putGroup;
const onCrudDelete = deleteGroup;

function onOpenEditor() {
  load();
}

function onCloseEditor() {
  table.row = {
    name: undefined,
    scopes: [],
  };
  // reset(categoriesDropdown);
  // reset(bucketsDropdown);
}
</script>

<template>
  <div class="views-setting-container">
    <crud-table
      class="w-full"
      :state="table"
      :editor-title="'Directory'"
      :headers="headers"
      :colspan="'3'"
      :on-crud-create="onCrudCreate"
      :on-crud-get="onCrudGet"
      :on-crud-get-total="onCrudGetTotal"
      :on-crud-update="onCrudUpdate"
      :on-crud-delete="onCrudDelete"
      :on-open-editor="onOpenEditor"
      :on-close-editor="onCloseEditor">
      <template v-slot:editor>
        <div class="modal-row h-10">
          <span class="w-32 mr-4">Name:</span>
          <input class="flex-1 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
        </div>
      </template>
    </crud-table>
  </div>
</template>
