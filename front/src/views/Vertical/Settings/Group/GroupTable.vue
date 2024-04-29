<script setup lang="ts">
import { watch } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownMode, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";
import { CrudTableState, Header } from "@/elements/Table/CrudTable/interface";

import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import CrudTable from "@/elements/Table/CrudTable/index.vue";

import {
    deleteGroup,
    getGroupTotal,
    getGroupWithScope,
    getGroups,
    postGroupWithScopeIDs,
    putGroupWithScopeIDs,
} from "@/api/v1/group";
import { getScopesStartsWith } from "@/api/v1/scope";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";

interface Row {
    id?: number;
    name: string;
    scope_ids?: Array<number>;
    scope_names?: Array<string>;
}

const scopes = initSelectDropdownState() as SelectDropdownState;
const onGetScopes = (param: any) => {
    param.name = "";
    return getScopesStartsWith(param);
};
function onGetScopesToOptions(data: { id: number; name: string }) {
    return { title: data.name, value: data.id };
}
watch(
    () => scopes.chips.length,
    () => {
        table.row.scope_ids = [];
        for (const chip of scopes.chips) {
            table.row.scope_ids.push(chip.value as number);
            table.row.scope_names.push(chip.title as string);
        }
    },
);

const table = initCrudTableState() as CrudTableState<Row>;

const headers: Array<Header> = [
    { title: "Id", key: "id" },
    { title: "Name", key: "name" },
];

const onCrudCreate = postGroupWithScopeIDs;
const onCrudGet = getGroups;
const onCrudGetTotal = getGroupTotal;
const onCrudUpdate = putGroupWithScopeIDs;
const onCrudDelete = deleteGroup;

function onOpenEditor() {
    const groupID = table.row.id;
    if (!groupID) {
        return;
    }
    getGroupWithScope(groupID).then((response) => {
        if (response.status === 200) {
            const groupWithScopes = response.data;
            table.row.scope_ids = groupWithScopes.scope_ids;
            table.row.scope_names = groupWithScopes.scope_names;
            scopes.chips = [];
            for (const i in table.row.scope_ids) {
                scopes.chips.push({ title: table.row.scope_names[i], value: table.row.scope_ids[i] });
            }
        }
    });
}

function onCloseEditor() {
    table.row = {
        name: undefined,
        scope_ids: [],
        scope_names: [],
    };
}
</script>

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
            :on-close-editor="onCloseEditor"
        >
            <template v-slot:editor>
                <div class="modal-row h-10">
                    <span class="w-32 mr-4">Name:</span>
                    <input
                        class="flex-1 modal-input"
                        type="text"
                        :placeholder="table.row.name"
                        v-model="table.row.name"
                    />
                </div>
                <div class="modal-row">
                    <span class="w-32 mr-4">Scopes:</span>
                    <select-dropdown
                        class="flex-1"
                        :options-width-class="'w-64'"
                        :origin="Origin.BottomLeft"
                        :state="scopes"
                        :enable-input-chips-enter-event="false"
                        :on-get="onGetScopes"
                        :on-get-to-options="onGetScopesToOptions"
                        :mode="SelectDropdownMode.InputChips"
                    />
                </div>
            </template>
        </crud-table>
    </div>
</template>
