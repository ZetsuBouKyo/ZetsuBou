<script setup lang="ts">
import { CrudGetParam } from "@/elements/Table/CrudTable/interface";
import { Row } from "./ElasticQueryTable.interface";

import ElasticQueryTable from "./ElasticQueryTable.vue";

import {
    deleteUserElasticCountQuery,
    getUserElasticCountQueries,
    getUserElasticCountQueryTotal,
    postUserElasticCountQuery,
    putUserElasticCountQuery,
} from "@/api/v1/user/elasticQuery/count";

import { userState } from "@/state/user";

const userID = userState.data.id;

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
</script>

<template>
    <div class="views-setting-container">
        <elastic-query-table
            :editor-title="editorTitle"
            :on-crud-create="onCrudCreate"
            :on-crud-get="onCrudGet"
            :on-crud-get-total="onCrudGetTotal"
            :on-crud-update="onCrudUpdate"
            :on-crud-delete="onCrudDelete"
        />
    </div>
</template>
