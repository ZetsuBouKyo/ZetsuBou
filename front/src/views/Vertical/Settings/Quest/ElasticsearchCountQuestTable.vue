<script setup lang="ts">
import { watch } from "vue";
import { useRouter } from "vue-router";

import { SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";
import { CrudTableState, Header } from "@/elements/Table/CrudTable/interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import CrudTable from "@/elements/Table/CrudTable/index.vue";

import { getUserElasticCountQueries, getUserElasticCountQuery } from "@/api/v1/user/elasticQuery/count";
import {
  deleteUserElasticCountQuest,
  getUserElasticCountQuestTotal,
  getUserElasticCountQuests,
  postUserElasticCountQuest,
  putUserElasticCountQuest,
} from "@/api/v1/user/quest/elasticCountQuest";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";
import { userState } from "@/state/user";

import { getDatetime } from "@/utils/datetime";

interface Row {
  id?: number;
  user_id?: number;
  name: string;
  numerator_id: number;
  denominator_id: number;
  created?: string;
  modified?: string;
}

const router = useRouter();

const userID = userState.id;
const table = initCrudTableState() as CrudTableState<Row>;

const numerator = initSelectDropdownState() as SelectDropdownState;
const denominator = initSelectDropdownState() as SelectDropdownState;
function onGet(params: PaginationGetParam) {
  return getUserElasticCountQueries(userID, params);
}
function onGetToOptions(data: { name: string | number; id: number }) {
  return { title: data.name, value: data.id };
}

watch(
  () => numerator.title,
  () => {
    if (numerator.title) {
      const numerator_id = numerator.selectedValue as number;
      table.row.numerator_id = numerator_id;
    }
  },
);

watch(
  () => {
    if (table.row) {
      return table.row.numerator_id;
    }
    return false;
  },
  () => {
    numerator.selectedValue = table.row.numerator_id;
    getUserElasticCountQuery(userID, numerator.selectedValue).then((response) => {
      const data = response.data;
      if (data) {
        numerator.title = data.name;
      }
    });
  },
);

watch(
  () => denominator.title,
  () => {
    if (denominator.title) {
      const denominator_id = denominator.selectedValue as number;
      table.row.denominator_id = denominator_id;
    }
  },
);

watch(
  () => {
    if (table.row) {
      return table.row.denominator_id;
    }
    return false;
  },
  () => {
    denominator.selectedValue = table.row.denominator_id;
    getUserElasticCountQuery(userID, denominator.selectedValue).then((response) => {
      const data = response.data;
      if (data) {
        denominator.title = data.name;
      }
    });
  },
);

function openQueryPage() {
  router.push("/settings/elasticsearch-count");
}

const headers: Array<Header> = [
  { title: "Id", key: "id" },
  { title: "Name", key: "name" },
  { title: "Numerator Id", key: "numerator_id" },
  { title: "Denominator Id", key: "denominator_id" },
  { title: "Created", key: "created", handler: getDatetime },
  { title: "Modified", key: "modified", handler: getDatetime },
];

function onCrudCreate(row: Row) {
  return postUserElasticCountQuest(userID, row);
}
function onCrudGet(params: PaginationGetParam) {
  return getUserElasticCountQuests(userID, params);
}
function onCrudGetTotal() {
  return getUserElasticCountQuestTotal(userID);
}
function onCrudUpdate(row: Row) {
  return putUserElasticCountQuest(userID, row);
}
function onCrudDelete(id: number) {
  return deleteUserElasticCountQuest(userID, id);
}

function onCloseEditor() {
  table.row = { name: undefined, numerator_id: undefined, denominator_id: undefined };
  numerator.reset();
  denominator.reset();
}
</script>

<template>
  <div class="views-setting-container">
    <crud-table
      class="w-full"
      :state="table"
      :editor-title="'Elastic Count Quest'"
      :headers="headers"
      :colspan="'8'"
      :on-crud-create="onCrudCreate"
      :on-crud-get="onCrudGet"
      :on-crud-get-total="onCrudGetTotal"
      :on-crud-update="onCrudUpdate"
      :on-crud-delete="onCrudDelete"
      :on-close-editor="onCloseEditor">
      <template v-slot:editor>
        <div class="modal-row">
          <span class="w-32 mr-4">Name:</span>
          <input class="w-1/2 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Numerator Id:</span>
          <select-dropdown
            class="h-10 w-64"
            :options-width-class="'w-64'"
            :state="numerator"
            :on-get="onGet"
            :on-get-to-options="onGetToOptions"></select-dropdown>
          <ripple-button class="ml-2 btn btn-primary" @click="openQueryPage"> Add </ripple-button>
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Denominator Id:</span>
          <select-dropdown
            class="h-10 w-64"
            :options-width-class="'w-64'"
            :state="denominator"
            :on-get="onGet"
            :on-get-to-options="onGetToOptions"></select-dropdown>
        </div>
      </template>
    </crud-table>
  </div>
</template>
