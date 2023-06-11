<template>
  <div class="views-setting-container">
    <crud-table
      class="w-full"
      :state="table"
      :editor-title="'Directory'"
      :headers="headers"
      :colspan="'3'"
      :on-crud-create="onCrudCreate"
      :on-crud-get="onCrudGet"
      :on-crud-get-total="onCrudGetTotal"
      :on-crud-update="onCrudUpdate"
      :on-crud-delete="onCrudDelete"
      :on-open-editor="onOpenEditor"
      :on-close-editor="onCloseEditor">
      <template v-slot:editor>
        <div class="modal-row">
          <span class="w-32 mr-4">Name:</span>
          <input class="flex-1 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
        </div>
      </template>
    </crud-table>
  </div>
</template>

<script lang="ts">
import { reactive, watch } from "vue";

import { getGroupTotal, getGroup, putGroup, postGroup, deleteGroup } from "@/api/v1/group";
import SelectDropdown, { SelectDropdownState, reset } from "@/elements/Dropdown/SelectDropdown.vue";

import CrudTable, { CrudTableState, Header } from "@/elements/Table/CrudTable/index.vue";

interface Scope {
  group_id: number;
  id: number;
  name?: string;
}

export interface Row {
  id?: number;
  name: string;
  scopes: Array<Scope>;
}

export default {
  components: { CrudTable, SelectDropdown },
  setup() {
    const table = CrudTable.initState() as CrudTableState<Row>;

    const prefix = reactive({
      options: [],
    });

    watch(
      () => table.row,
      () => {
        // const bucketName = bucketsDropdown.selectedValue as string;
        // const prefixName = table.row.prefix as string;
        // if (bucketName === undefined || prefixName === undefined) {
        //   return;
        // }
        // if (prefixName.slice(-1) === "/") {
        //   getPrefixAutoComplete(bucketName, prefixName);
        // }
      },
    );

    function load() {
      // getMinioStorageCategories().then((response) => {
      //   const data = response.data;
      //   if (data) {
      //     for (let key in data) {
      //       categoriesDropdown.options.push({ title: key, value: data[key] });
      //     }
      //   }
      // });
    }

    const headers: Array<Header> = [
      { title: "Id", key: "id" },
      { title: "Name", key: "name" },
    ];

    const onCrudCreate = postGroup;
    const onCrudGet = getGroup;
    const onCrudGetTotal = getGroupTotal;
    const onCrudUpdate = putGroup;
    const onCrudDelete = deleteGroup;

    function onOpenEditor() {
      load();
    }

    function onCloseEditor() {
      table.row = {
        name: undefined,
        scopes: [],
      };
      // reset(categoriesDropdown);
      // reset(bucketsDropdown);
    }

    return {
      table,
      headers,
      prefix,
      onCrudCreate,
      onCrudGet,
      onCrudGetTotal,
      onCrudUpdate,
      onCrudDelete,
      onOpenEditor,
      onCloseEditor,
    };
  },
};
</script>
