<script setup lang="ts">
import { watch } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownMode, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";
import { CrudTableState, Header } from "@/elements/Table/CrudTable/interface";

import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import CrudTable from "@/elements/Table/CrudTable/index.vue";

import { getGroups } from "@/api/v1/group";
import { deleteUser, getUsers, getUsersTotal, postUserWithGroups, putUserWithGroups } from "@/api/v1/user/user";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";

import { messageState } from "@/state/message";

import { getDatetime } from "@/utils/datetime";
import { joinWithAnd } from "@/utils/str";

interface Row {
    id?: number;
    name: string;
    email: string;
    created?: string;
    last_signin?: string;
    password?: string;
    new_password?: string;
    group_ids?: Array<number>;
    group_names?: Array<string>;
}

const table = initCrudTableState() as CrudTableState<Row>;

function getHeaderGroups(groupNames: Array<string>) {
    return groupNames.join(", ");
}
const headers: Array<Header> = [
    { title: "Id", key: "id" },
    { title: "Name", key: "name" },
    { title: "Email", key: "email" },
    { title: "Groups", key: "group_names", handler: getHeaderGroups },
    { title: "Created", key: "created", handler: getDatetime },
    { title: "Last_signin", key: "last_signin", handler: getDatetime },
];

const groups = initSelectDropdownState() as SelectDropdownState;
const onGetTokens = getGroups;
function onGetTokensToOptions(data: { name: string | number; id: number }) {
    return { title: data.name, value: data.id };
}
function onOpenEditor() {
    groups.chips = [];
    for (const i in table.row.group_ids) {
        groups.chips.push({ title: table.row.group_names[i], value: table.row.group_ids[i] });
    }
}
watch(
    () => groups.chips.length,
    () => {
        table.row.group_ids = [];
        for (const chip of groups.chips) {
            table.row.group_ids.push(chip.value as number);
            table.row.group_names.push(chip.title as string);
        }
    },
);

function checkInput(row: Row): boolean {
    const inputs = [];
    if (!row.name) {
        inputs.push("name");
    }
    if (!row.email) {
        inputs.push("email");
    }
    if (!row.password) {
        inputs.push("password");
    }
    if (inputs.length > 0) {
        const s = joinWithAnd(inputs);
        const msg = `Please enter ${s}.`;
        messageState.push(msg);
        return false;
    }

    return true;
}
const onCrudCreate = (row: Row) => {
    const c = checkInput(row);
    if (!c) {
        return;
    }
    if (row.group_ids === undefined) {
        row.group_ids = [];
    }
    return postUserWithGroups(row);
};
const onCrudGet = getUsers;
const onCrudGetTotal = getUsersTotal;
const onCrudUpdate = (row: Row) => {
    const c = checkInput(row);
    if (!c) {
        return;
    }
    if (row.group_ids === undefined) {
        row.group_ids = [];
    }

    return putUserWithGroups(row.id, row);
};
const onCrudDelete = deleteUser;
</script>

<template>
    <div class="views-setting-container">
        <crud-table
            class="w-full"
            :state="table"
            :editor-title="'User'"
            :headers="headers"
            :colspan="'7'"
            :on-crud-create="onCrudCreate"
            :on-crud-get="onCrudGet"
            :on-crud-get-total="onCrudGetTotal"
            :on-crud-update="onCrudUpdate"
            :on-crud-delete="onCrudDelete"
            :on-open-editor="onOpenEditor"
            :delete-confirm-message="'Are you sure you want to permanently delete this row? This might destroy the database.'"
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
                <div class="modal-row h-10">
                    <span class="w-32 mr-4">Email:</span>
                    <input
                        class="flex-1 modal-input"
                        type="text"
                        :placeholder="table.row.email"
                        v-model="table.row.email"
                    />
                </div>
                <div class="modal-row">
                    <span class="w-32 mr-4">Groups:</span>
                    <select-dropdown
                        class="flex-1"
                        :options-width-class="'w-64'"
                        :origin="Origin.BottomLeft"
                        :state="groups"
                        :enable-input-chips-enter-event="false"
                        :on-get="onGetTokens"
                        :on-get-to-options="onGetTokensToOptions"
                        :mode="SelectDropdownMode.InputChips"
                    />
                </div>
                <div class="modal-row h-10">
                    <span class="w-32 mr-4">Password:</span>
                    <input
                        class="flex-1 modal-input"
                        type="password"
                        autocomplete="new-password"
                        :placeholder="table.row.password"
                        v-model="table.row.password"
                    />
                </div>
            </template>
            <template v-slot:editor-update>
                <div class="modal-row h-10">
                    <span class="w-32 mr-4">New password:</span>
                    <input
                        class="flex-1 modal-input"
                        type="password"
                        autocomplete="new-password"
                        :placeholder="table.row.new_password"
                        v-model="table.row.new_password"
                    />
                </div>
            </template>
        </crud-table>
    </div>
</template>
