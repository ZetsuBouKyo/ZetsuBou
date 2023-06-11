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

<script lang="ts">
import { defineComponent } from "vue";

import { userState } from "@/state/user";

import {
  getUserElasticCountQueryTotal,
  getUserElasticCountQueries,
  postUserElasticCountQuery,
  putUserElasticCountQuery,
  deleteUserElasticCountQuery,
} from "@/api/v1/user/elasticQuery/count";

import ElasticQueryTable, { Row } from "./ElasticQueryTable.vue";
import { GetParam } from "@/elements/Table/CrudTable/index.vue";

export default defineComponent({
  components: { ElasticQueryTable },
  setup() {
    const userID = userState.id;

    function onCrudCreate(row: Row) {
      return postUserElasticCountQuery(userID, row);
    }
    function onCrudGet(params: GetParam) {
      return getUserElasticCountQueries(userID, params);
    }
    function onCrudGetTotal() {
      return getUserElasticCountQueryTotal(userID);
    }
    function onCrudUpdate(row: Row) {
      return putUserElasticCountQuery(userID, row);
    }
    function onCrudDelete(id: number) {
      return deleteUserElasticCountQuery(userID, id);
    }

    const editorTitle = "Elastic Count Query";

    return { editorTitle, onCrudCreate, onCrudGet, onCrudGetTotal, onCrudUpdate, onCrudDelete };
  },
});
</script>
