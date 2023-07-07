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
  deleteUserElasticCountQuery,
  getUserElasticCountQueries,
  getUserElasticCountQueryTotal,
  postUserElasticCountQuery,
  putUserElasticCountQuery,
} from "@/api/v1/user/elasticQuery/count";

import { CrudGetParam } from "@/elements/Table/CrudTable/index.vue";
import ElasticQueryTable, { Row } from "./ElasticQueryTable.vue";

export default defineComponent({
  components: { ElasticQueryTable },
  setup() {
    const userID = userState.id;

    function onCrudCreate(row: Row) {
      return postUserElasticCountQuery(userID, row);
    }
    function onCrudGet(params: CrudGetParam) {
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
