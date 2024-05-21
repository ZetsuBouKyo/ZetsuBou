<script setup lang="ts">
import { ref, Ref, watch } from "vue";
import { useRouter } from "vue-router";

import { SelectDropdownOption } from "@/elements/Dropdown/SelectDropdown.interface";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";
import { CrudTableState, Header } from "@/elements/Table/CrudTable/interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import RippleButtonSelectDropdown from "@/elements/Dropdown/RippleButtonSelectDropdown.vue";
import CrudTable from "@/elements/Table/CrudTable/index.vue";

import { getUserElasticCountQueries, getUserElasticCountQuery } from "@/api/v1/user/elasticQuery/count";
import {
  deleteUserElasticCountQuest,
  getUserElasticCountQuestTotal,
  getUserElasticCountQuests,
  postUserElasticCountQuest,
  putUserElasticCountQuest,
} from "@/api/v1/user/quest/elasticCountQuest";

import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";
import { userState } from "@/state/user";

import { getDatetime } from "@/utils/datetime";
import { getFirstOptions, scroll, convertArrayDataToOptions } from "@/elements/Dropdown/SelectDropdown";

interface T {
  id: number;
  name: string | number;
}

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

const userID = userState.data.id;
const table = initCrudTableState() as CrudTableState<Row>;

function getQuery(params: PaginationGetParam) {
  return getUserElasticCountQueries(userID, params);
}
function convert(data: Array<T>, options: Ref<Array<SelectDropdownOption>>) {
  convertArrayDataToOptions<T>(
    (d: T) => {
      return { title: d.name, value: d.id };
    },
    data,
    options,
  );
}

const numerator = ref();
const numeratorTitle = ref("");
const numeratorSelectedValue = ref(undefined);
const numeratorOptions = ref([]);
const numeratorScrollEnd = ref<boolean>(false);

const numeratorParams = ref<PaginationGetParam>({
  page: 1,
  size: 20,
});
const numeratorLock = ref<boolean>(false);

function selectNumerator(opt: SelectDropdownOption) {
  table.row.numerator_id = opt.value as number;
}

function openNumerator() {
  getFirstOptions(getQuery, convert, numeratorParams, numeratorOptions, numeratorLock, numeratorScrollEnd);
}

function scrollNumerator(event: any) {
  scroll(event, getQuery, convert, numeratorParams, numeratorOptions, numeratorLock, numeratorScrollEnd);
}

const denominator = ref();
const denominatorTitle = ref("");
const denominatorSelectedValue = ref(undefined);
const denominatorOptions = ref([]);
const denominatorScrollEnd = ref<boolean>(false);

const denominatorParams = ref<PaginationGetParam>({
  page: 1,
  size: 20,
});
const denominatorLock = ref<boolean>(false);

function selectDenominator(opt: SelectDropdownOption) {
  table.row.denominator_id = opt.value as number;
}

function openDenominator() {
  getFirstOptions(getQuery, convert, denominatorParams, denominatorOptions, denominatorLock, denominatorScrollEnd);
}

function scrollDenominator(event: any) {
  scroll(event, getQuery, convert, denominatorParams, denominatorOptions, denominatorLock, denominatorScrollEnd);
}

watch(
  () => {
    return JSON.stringify(table.row);
  },
  () => {
    if (!userID) {
      return;
    }
    numeratorSelectedValue.value = table.row.numerator_id;
    if (numeratorSelectedValue.value !== undefined) {
      getUserElasticCountQuery(userID, numeratorSelectedValue.value).then((response) => {
        const data = response.data;
        if (data) {
          numeratorTitle.value = data.name;
        }
      });
    }

    denominatorSelectedValue.value = table.row.denominator_id;
    if (denominatorSelectedValue.value !== undefined) {
      getUserElasticCountQuery(userID, denominatorSelectedValue.value).then((response) => {
        const data = response.data;
        if (data) {
          denominatorTitle.value = data.name;
        }
      });
    }
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
  numerator.value.clear();
  denominator.value.clear();
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
        <div class="modal-row h-10">
          <span class="w-32 mr-4">Name:</span>
          <input class="w-1/2 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
        </div>
        <div class="modal-row h-10">
          <span class="w-32 mr-4">Numerator Id:</span>
          <ripple-button-select-dropdown
            ref="numerator"
            class="h-10 w-64"
            v-model:title="numeratorTitle"
            v-model:selected-value="numeratorSelectedValue"
            v-model:options="numeratorOptions"
            v-model:scroll-end="numeratorScrollEnd"
            :options-width-class="'w-64'"
            :on-open="openNumerator"
            :on-scroll="scrollNumerator"
            :on-select="selectNumerator" />
          <ripple-button class="ml-2 btn btn-primary" @click="openQueryPage"> Add </ripple-button>
        </div>
        <div class="modal-row h-10">
          <span class="w-32 mr-4">Denominator Id:</span>
          <ripple-button-select-dropdown
            ref="denominator"
            class="h-10 w-64"
            v-model:title="denominatorTitle"
            v-model:selected-value="denominatorSelectedValue"
            v-model:options="denominatorOptions"
            v-model:scroll-end="denominatorScrollEnd"
            :options-width-class="'w-64'"
            :on-open="openDenominator"
            :on-scroll="scrollDenominator"
            :on-select="selectDenominator" />
        </div>
      </template>
    </crud-table>
  </div>
</template>
