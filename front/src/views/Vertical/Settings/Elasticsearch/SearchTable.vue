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
  deleteUserElasticSearchQuery,
  getUserElasticSearchQueries,
  getUserElasticSearchQueryTotal,
  postUserElasticSearchQuery,
  putUserElasticSearchQuery,
} from "@/api/v1/user/elasticQuery/search";

import { CrudGetParam } from "@/elements/Table/CrudTable/index.vue";
import ElasticQueryTable, { Row } from "./ElasticQueryTable.vue";

export default defineComponent({
  components: { ElasticQueryTable },
  setup() {
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

    return { editorTitle, onCrudCreate, onCrudGet, onCrudGetTotal, onCrudUpdate, onCrudDelete };
  },
});
</script>
