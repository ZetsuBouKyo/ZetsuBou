<script setup lang="ts">
import { reactive, ref, Ref } from "vue";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownOption } from "@/elements/Dropdown/SelectDropdown.interface";
import { PaginationGetParam } from "@/elements/Pagination/pagination.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import InputChipSelectDropdown from "@/elements/Dropdown/InputChipSelectDropdown.vue";

import { getScopesStartsWith } from "@/api/v1/scope";
import { getToken } from "@/api/v1/token";

import { getFirstOptions, scroll, convertArrayDataToOptions } from "@/elements/Dropdown/SelectDropdown";

import { JWTParser } from "@/utils/jwt";

const state = reactive({
    email: undefined,
    password: undefined,
    expires: 30 as any,
    token: undefined,
    scopes: [],
    header: undefined,
    payload: undefined,
});

function getNewToken() {
    const scope = state.scopes.join(" ");

    const formData = new FormData();
    formData.append("username", state.email);
    formData.append("password", state.password);
    formData.append("expires", state.expires);
    formData.append("scope", scope);

    getToken(formData).then((response) => {
        const data = response.data;
        if (data) {
            state.token = data.access_token;
            const parser = new JWTParser(state.token);
            state.header = parser.headerString;
            state.payload = parser.payloadString;
        }
    });
}

interface ScopeT {
    id: number;
    name: string;
}
interface ScopeSelectDropdownGetParam extends PaginationGetParam {
    name: string;
}
const scopeTitle = ref("");
const scopeSelectedValue = ref(undefined);
const scopeChips = ref([]);
const scopeOptions = ref([]);
const scopeScrollEnd = ref<boolean>(false);

const scopeParams = ref<ScopeSelectDropdownGetParam>({ page: 1, size: 20, name: "" });
const scopeLock = ref<boolean>(false);

function convertScope(data: Array<ScopeT>, options: Ref<Array<SelectDropdownOption>>) {
    convertArrayDataToOptions<ScopeT>(
        (d: ScopeT) => {
            return { title: d.name, value: d.id };
        },
        data,
        options,
    );
}
async function getScope(params: PaginationGetParam) {
    return getScopesStartsWith(params);
}
function deleteChipScope(title: string, _: number, __: number) {
    const i = state.scopes.indexOf(title);
    if (i === -1) {
        return;
    }
    state.scopes.splice(i, 1);
}
function inputScope(s: string) {
    scopeParams.value.name = s;
    openScope();
}
function openScope() {
    getFirstOptions(getScope, convertScope, scopeParams, scopeOptions, scopeLock, scopeScrollEnd);
}
function scrollScope(event: any) {
    scroll(event, getScope, convertScope, scopeParams, scopeOptions, scopeLock, scopeScrollEnd);
}
function selectScope(opt: SelectDropdownOption) {
    state.scopes.push(opt.title);
}
</script>

<template>
    <div class="views-setting-container">
        <div class="views-setting-section">
            <span class="views-setting-section-title">Token</span>
            <div class="views-setting-rows">
                <div class="views-setting-row-12">
                    <div class="views-setting-cell w-48">Email address:</div>
                    <input class="views-setting-cell w-72" type="text" v-model="state.email" />
                </div>
                <div class="views-setting-row-12">
                    <div class="views-setting-cell w-48">Password:</div>
                    <input
                        class="views-setting-cell w-72"
                        type="password"
                        autocomplete="new-password"
                        v-model="state.password"
                    />
                </div>
                <div class="views-setting-row-12">
                    <div class="views-setting-cell w-48">Expires in minutes:</div>
                    <input
                        class="views-setting-cell w-72"
                        :placeholder="state.expires"
                        type="text"
                        v-model="state.expires"
                    />
                </div>
                <div class="views-setting-row items-start">
                    <div class="views-setting-cell w-48 my-4">Scopes:</div>
                    <input-chip-select-dropdown
                        class="flex-1 ml-1"
                        v-model:title="scopeTitle"
                        v-model:selected-value="scopeSelectedValue"
                        v-model:chips="scopeChips"
                        v-model:options="scopeOptions"
                        v-model:scroll-end="scopeScrollEnd"
                        :options-width-class="'w-64'"
                        :origin="Origin.BottomLeft"
                        :enable-input-chips-enter-event="false"
                        :on-delete-chip="deleteChipScope"
                        :on-input="inputScope"
                        :on-open="openScope"
                        :on-scroll="scrollScope"
                        :on-select="selectScope"
                    />
                </div>
                <div class="views-setting-row-12">
                    <ripple-button class="flex btn btn-primary ml-auto" @click="getNewToken">Get</ripple-button>
                </div>
                <div class="views-setting-row items-start" v-if="state.token">
                    <div class="views-setting-cell w-48">Token:</div>
                    <div class="flex w-96 2xl:w-200 break-all">{{ state.token }}</div>
                </div>
                <div class="views-setting-row items-start" v-if="state.header">
                    <div class="views-setting-cell w-48">Token Header:</div>
                    <pre>{{ state.header }}</pre>
                </div>
                <div class="views-setting-row items-start" v-if="state.payload">
                    <div class="views-setting-cell w-48">Token Payload:</div>
                    <pre>{{ state.payload }}</pre>
                </div>
            </div>
        </div>
    </div>
</template>
