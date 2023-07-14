<script setup lang="ts">
import { CrudGetParam } from "@/elements/Table/CrudTable/interface";
import { Row } from "./ElasticQueryTable.interface";

import ElasticQueryTable from "./ElasticQueryTable.vue";

import {
  deleteUserElasticSearchQuery,
  getUserElasticSearchQueries,
  getUserElasticSearchQueryTotal,
  postUserElasticSearchQuery,
  putUserElasticSearchQuery,
} from "@/api/v1/user/elasticQuery/search";

import { userState } from "@/state/user";

const userID = userState.id;

function onCrudCreate(row: Row) {
  return postUserElasticSearchQuery(userID, row);
}
function onCrudGet(params: CrudGetParam) {
  return getUserElasticSearchQueries(userID, params);
}
function onCrudGetTotal() {
  return getUserElasticSearchQueryTotal(userID);
}
function onCrudUpdate(row: Row) {
  return putUserElasticSearchQuery(userID, row);
}
function onCrudDelete(id: number) {
  return deleteUserElasticSearchQuery(userID, id);
}

const editorTitle = "Elastic Search Query";
</script>

<template>
  <div class="views-setting-container">
    <elastic-query-table
      :editor-title="editorTitle"
      :on-crud-create="onCrudCreate"
      :on-crud-get="onCrudGet"
      :on-crud-get-total="onCrudGetTotal"
      :on-crud-update="onCrudUpdate"
      :on-crud-delete="onCrudDelete" />
  </div>
</template>
