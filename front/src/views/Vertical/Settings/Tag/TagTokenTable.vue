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
      :delete-confirm-message="'Are you sure you want to permanently delete this row? This might destroy the database.'">
      <template v-slot:editor>
        <div class="modal-row">
          <span class="w-32 mr-4">Name:</span>
          <input class="w-1/2 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
        </div>
      </template>
    </crud-table>
  </div>
</template>

<script lang="ts">
import CrudTable, { CrudTableState, Header } from "@/elements/Table/CrudTable/index.vue";

import { getTagTokenTotal, getTagTokens, postTagToken, putTagToken, deleteTagToken } from "@/api/v1/tag/token";

export interface Row {
  id?: number;
  name: string;
}

export default {
  components: { CrudTable },
  setup() {
    const table = CrudTable.initState() as CrudTableState<Row>;
    const headers: Array<Header> = [
      { title: "Id", key: "id" },
      { title: "Name", key: "name" },
    ];

    const onCrudCreate = postTagToken;
    const onCrudGet = getTagTokens;
    const onCrudGetTotal = getTagTokenTotal;
    const onCrudUpdate = putTagToken;
    const onCrudDelete = deleteTagToken;

    return { table, headers, onCrudCreate, onCrudGet, onCrudGetTotal, onCrudUpdate, onCrudDelete };
  },
};
</script>
