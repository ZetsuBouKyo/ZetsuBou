<script setup lang="ts">
import { CrudTableState, Header } from "@/elements/Table/CrudTable/interface";

import CrudTable from "@/elements/Table/CrudTable/index.vue";

import { deleteTagToken, getTagTokenTotal, getTagTokens, postTagToken, putTagToken } from "@/api/v1/tag/token";

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

const onCrudCreate = postTagToken;
const onCrudGet = getTagTokens;
const onCrudGetTotal = getTagTokenTotal;
const onCrudUpdate = putTagToken;
const onCrudDelete = deleteTagToken;
</script>

<template>
    <div class="views-setting-container">
        <crud-table
            class="w-full"
            :state="table"
            :editor-title="'Tag Token'"
            :headers="headers"
            :colspan="'3'"
            :on-crud-create="onCrudCreate"
            :on-crud-get="onCrudGet"
            :on-crud-get-total="onCrudGetTotal"
            :on-crud-update="onCrudUpdate"
            :on-crud-delete="onCrudDelete"
            :delete-confirm-message="'Are you sure you want to permanently delete this row? This might destroy the database.'"
        >
            <template v-slot:editor>
                <div class="modal-row h-10">
                    <span class="w-32 mr-4">Name:</span>
                    <input
                        class="w-1/2 modal-input"
                        type="text"
                        :placeholder="table.row.name"
                        v-model="table.row.name"
                    />
                </div>
            </template>
        </crud-table>
    </div>
</template>
