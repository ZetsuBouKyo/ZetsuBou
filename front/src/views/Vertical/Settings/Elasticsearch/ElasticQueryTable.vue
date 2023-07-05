<template>
  <crud-table
    class="w-full"
    :state="table"
    :editor-title="editorTitle"
    :headers="headers"
    :colspan="'5'"
    :on-crud-create="onCrudCreate"
    :on-crud-get="onCrudGet"
    :on-crud-get-total="onCrudGetTotal"
    :on-crud-update="onCrudUpdate"
    :on-crud-delete="onCrudDelete">
    <template v-slot:editor>
      <div class="modal-row">
        <span class="w-24 mr-4">Name:</span>
        <input class="flex-1 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
      </div>
      <div class="modal-row">
        <span class="w-24 mr-4">Template:</span>
        <select-dropdown
          class="h-10 w-64"
          :options-width-class="'w-64'"
          :origin="Origin.BottomLeft"
          :state="examples"
          :on-select="onSelect"
          :enable-input-chips-enter-event="false" />
      </div>
      <div class="modal-row h-56">
        <textarea v-model="table.row.query" class="modal-textarea h-full" />
      </div>
    </template>
  </crud-table>
</template>

<script lang="ts">
import { PropType } from "vue";

import { getDatetime } from "@/utils/datetime";

import { getQueryExample } from "@/api/v1/elasticsearch";

import CrudTable, {
  CrudTableState,
  Header,
  OnCrudCreate,
  OnCrudDelete,
  OnCrudGet,
  OnCrudGetTotal,
  OnCrudUpdate,
} from "@/elements/Table/CrudTable/index.vue";

import SelectDropdown, {
  Origin,
  SelectDropdownOption,
  SelectDropdownState,
} from "@/elements/Dropdown/SelectDropdown.vue";

export interface Row {
  id?: number;
  user_id?: number;
  name: string;
  query: string;
  created?: string;
  modified?: string;
}

export default {
  components: { CrudTable, SelectDropdown },
  props: {
    editorTitle: {
      type: Object as PropType<string>,
      default: undefined,
    },
    onCrudCreate: {
      type: Object as PropType<OnCrudCreate>,
      default: undefined,
    },
    onCrudGet: {
      type: Object as PropType<OnCrudGet>,
      default: undefined,
    },
    onCrudGetTotal: {
      type: Object as PropType<OnCrudGetTotal>,
      default: undefined,
    },
    onCrudUpdate: {
      type: Object as PropType<OnCrudUpdate>,
      default: undefined,
    },
    onCrudDelete: {
      type: Object as PropType<OnCrudDelete>,
      default: undefined,
    },
  },
  setup(props) {
    const table = CrudTable.initState() as CrudTableState<Row>;
    const headers: Array<Header> = [
      { title: "Id", key: "id" },
      { title: "Name", key: "name" },
      { title: "Created", key: "created", handler: getDatetime },
      { title: "Modified", key: "modified", handler: getDatetime },
    ];

    const examples = SelectDropdown.initState() as SelectDropdownState;

    function onSelect(opt: SelectDropdownOption) {
      table.row.query = JSON.stringify(opt.raw.value, null, 4);
    }

    function loadExample() {
      getQueryExample().then((response) => {
        const data = response.data;
        for (const q of data) {
          const option: SelectDropdownOption = {
            title: q.summary,
            value: q.summary,
            raw: q,
          };
          examples.options.push(option);
        }
      });
    }
    loadExample();

    return { ...props, table, headers, examples, onSelect, Origin };
  },
};
</script>
