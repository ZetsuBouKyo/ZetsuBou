<script setup lang="ts">
import { CrudTableState, Header } from "@/elements/Table/CrudTable/interface";

import CrudTable from "@/elements/Table/CrudTable/index.vue";

import {
  deleteTagAttribute,
  getTagAttributeTotal,
  getTagAttributes,
  postTagAttribute,
  putTagAttribute,
} from "@/api/v1/tag/attribute";

import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";

interface Row {
  id?: number;
  name: string;
}

const table = initCrudTableState() as CrudTableState<Row>;
const headers: Array<Header> = [
  { title: "Id", key: "id" },
  { title: "Name", key: "name" },
];

const onCrudCreate = postTagAttribute;
const onCrudGet = getTagAttributes;
const onCrudGetTotal = getTagAttributeTotal;
const onCrudUpdate = putTagAttribute;
const onCrudDelete = deleteTagAttribute;
</script>

<template>
  <div class="views-setting-container">
    <crud-table
      class="w-full"
      :state="table"
      :editor-title="'Tag Attribute'"
      :headers="headers"
      :colspan="'3'"
      :on-crud-create="onCrudCreate"
      :on-crud-get="onCrudGet"
      :on-crud-get-total="onCrudGetTotal"
      :on-crud-update="onCrudUpdate"
      :on-crud-delete="onCrudDelete"
      :delete-confirm-message="'Are you sure you want to permanently delete this row? This might destroy the database.'">
      <template v-slot:editor>
        <div class="modal-row h-10">
          <span class="w-32 mr-4">Name:</span>
          <input class="w-1/2 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
        </div>
      </template>
    </crud-table>
  </div>
</template>
