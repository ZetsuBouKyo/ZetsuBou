<script setup lang="ts">
import { reactive, ref, Ref, watch } from "vue";
import { useRouter } from "vue-router";

import { SelectDropdownGetParam, SelectDropdownOption } from "@/elements/Dropdown/SelectDropdown.interface";
import { CrudTableState, Header } from "@/elements/Table/CrudTable/interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import RippleButtonSelectDropdown from "@/elements/Dropdown/RippleButtonSelectDropdown.vue";
import CrudTable from "@/elements/Table/CrudTable/index.vue";

import { getSettingUserQuestCategories } from "@/api/v1/setting/userQuestCategory";
import { getUserElasticCountQuest, getUserElasticCountQuests } from "@/api/v1/user/quest/elasticCountQuest";
import {
    deleteUserQuest,
    getUserQuestTotal,
    getUserQuests,
    postUserQuest,
    putUserQuest,
} from "@/api/v1/user/quest/quest";

import { initCrudTableState } from "@/elements/Table/CrudTable/CrudTable";
import { userState } from "@/state/user";

import { getDatetime } from "@/utils/datetime";
import { getFirstOptions, scroll, convertArrayDataToOptions } from "@/elements/Dropdown/SelectDropdown";

interface T {
    id: number;
    name: string | number;
}

interface Row {
    id?: number;
    user_id?: number;
    name: string;
    category_id: number;
    quest_id: number;
    priority: number;
    created?: string;
    modified?: string;
}

const router = useRouter();

const userID = userState.data.id;
const table = initCrudTableState() as CrudTableState<Row>;

const state = reactive({
    questUrl: undefined,
    onGetQuest: undefined,
});

function convert(data: Array<T>, options: Ref<Array<SelectDropdownOption>>) {
    convertArrayDataToOptions<T>(
        (d: T) => {
            return { title: d.name, value: d.id };
        },
        data,
        options,
    );
}

const category = ref();
const categoryTitle = ref("");
const categorySelectedValue = ref(undefined);
const categoryOptions = ref([]);
const categoryScrollEnd = ref<boolean>(false);

const categoryParams = ref<SelectDropdownGetParam>({
    page: 1,
    size: 20,
    s: "",
});
const categoryLock = ref<boolean>(false);

function getCategory(params: SelectDropdownGetParam) {
    return getSettingUserQuestCategories(params);
}

function openCategory() {
    getFirstOptions(getCategory, convert, categoryParams, categoryOptions, categoryLock, categoryScrollEnd);
}

function scrollCategory(event: any) {
    scroll(event, getQuest, convert, categoryParams, categoryOptions, categoryLock, categoryScrollEnd);
}

const quest = ref();
const questTitle = ref("");
const questSelectedValue = ref(undefined);
const questOptions = ref([]);
const questScrollEnd = ref<boolean>(false);

const questParams = ref<SelectDropdownGetParam>({
    page: 1,
    size: 20,
    s: "",
});
const questLock = ref<boolean>(false);

function getQuest(params: SelectDropdownGetParam) {
    return state.onGetQuest(params);
}

function openQuest() {
    getFirstOptions(getQuest, convert, questParams, questOptions, questLock, questScrollEnd);
}

function scrollQuest(event: any) {
    scroll(event, getQuest, convert, questParams, questOptions, questLock, questScrollEnd);
}

function selectCategory(opt: SelectDropdownOption) {
    state.questUrl = undefined;
    questOptions.value = [];
    if (opt.title) {
        const categoryId = opt.value as number;
        table.row.category_id = categoryId;
        switch (categoryId) {
            case 1:
                state.onGetQuest = (params: any) => {
                    return getUserElasticCountQuests(userID, params);
                };
                state.questUrl = "/settings/elasticsearch-count-quest";
                break;
        }
    }
}

function selectQuest(opt: SelectDropdownOption) {
    table.row.quest_id = opt.value as number;
}

watch(
    () => {
        return JSON.stringify(table.row);
    },
    () => {
        const categoryID = table.row.category_id;
        if (categoryID !== undefined) {
            categoryTitle.value = getCategoryName(categoryID);
            categorySelectedValue.value = categoryID;
            switch (categoryID) {
                case 1:
                    state.onGetQuest = (params: any) => {
                        return getUserElasticCountQuests(userID, params);
                    };
                    state.questUrl = "/settings/elasticsearch-count-quest";
                    break;
            }
        }

        const questID = table.row.quest_id;
        questSelectedValue.value = questID;
        if (questID !== undefined) {
            getUserElasticCountQuest(userID, questID).then((response) => {
                const data = response.data;
                if (data) {
                    questTitle.value = data.name;
                }
            });
        }
    },
);

function openQuestPage() {
    router.push(state.questUrl);
}

function onCloseEditor() {
    table.row = {
        name: undefined,
        category_id: undefined,
        quest_id: undefined,
        priority: undefined,
    };
    category.value.clear();
    quest.value.clear();
}

const categoryMap = reactive({});
const params = {
    page: 1,
    size: 20,
};
function getCategories(params: any) {
    getSettingUserQuestCategories(params).then((response) => {
        const data = response.data;
        if (data) {
            for (let i = 0; i < data.length; i++) {
                const title = data[i].name;
                const value = data[i].id;
                categoryMap[value] = title;
            }
            if (data.length > 0) {
                params.page++;
                getCategories(params);
            }
        }
    });
}
getCategories(params);
function getCategoryName(id: number) {
    return categoryMap[id];
}
const headers: Array<Header> = [
    { title: "Id", key: "id" },
    { title: "Name", key: "name" },
    { title: "Category", key: "category_id", handler: getCategoryName },
    { title: "Quest Id", key: "quest_id" },
    { title: "Priority", key: "priority" },
    { title: "Created", key: "created", handler: getDatetime },
    { title: "Modified", key: "modified", handler: getDatetime },
];

function onCrudCreate(row: Row) {
    return postUserQuest(userID, row);
}
function onCrudGet(params: SelectDropdownGetParam) {
    return getUserQuests(userID, params);
}
function onCrudGetTotal() {
    return getUserQuestTotal(userID);
}
function onCrudUpdate(row: Row) {
    return putUserQuest(userID, row);
}
function onCrudDelete(id: number) {
    return deleteUserQuest(userID, id);
}
</script>

<template>
    <div class="views-setting-container">
        <crud-table
            class="w-full"
            :state="table"
            :editor-title="'Quest'"
            :headers="headers"
            :colspan="'8'"
            :on-crud-create="onCrudCreate"
            :on-crud-get="onCrudGet"
            :on-crud-get-total="onCrudGetTotal"
            :on-crud-update="onCrudUpdate"
            :on-crud-delete="onCrudDelete"
            :on-close-editor="onCloseEditor"
        >
            <template v-slot:editor>
                <div class="modal-row h-10">
                    <span class="w-20 mr-4">Name:</span>
                    <input
                        class="w-1/2 modal-input"
                        type="text"
                        :placeholder="table.row.name"
                        v-model="table.row.name"
                    />
                </div>
                <div class="modal-row h-10">
                    <span class="w-20 mr-4">Category:</span>
                    <ripple-button-select-dropdown
                        ref="category"
                        class="h-10 w-64"
                        v-model:title="categoryTitle"
                        v-model:selected-value="categorySelectedValue"
                        v-model:options="categoryOptions"
                        v-model:scroll-end="categoryScrollEnd"
                        :options-width-class="'w-64'"
                        :on-open="openCategory"
                        :on-scroll="scrollCategory"
                        :on-select="selectCategory"
                    />
                </div>
                <div class="modal-row h-10" v-if="categoryTitle">
                    <span class="w-20 mr-4">Quest Id:</span>
                    <ripple-button-select-dropdown
                        ref="quest"
                        class="h-10 w-64"
                        v-model:title="questTitle"
                        v-model:selected-value="questSelectedValue"
                        v-model:options="questOptions"
                        v-model:scroll-end="questScrollEnd"
                        :options-width-class="'w-64'"
                        :on-open="openQuest"
                        :on-scroll="scrollQuest"
                        :on-select="selectQuest"
                    />
                    <ripple-button class="ml-2 btn btn-primary" @click="openQuestPage"> Add </ripple-button>
                </div>
                <div class="modal-row h-10" v-else></div>
                <div class="modal-row h-10" v-if="categoryTitle">
                    <span class="w-20 mr-4">Priority:</span>
                    <input
                        class="w-1/2 modal-input"
                        type="text"
                        :placeholder="table.row.priority as any"
                        v-model="table.row.priority"
                    />
                </div>
                <div class="modal-row h-10" v-else></div>
            </template>
        </crud-table>
    </div>
</template>
