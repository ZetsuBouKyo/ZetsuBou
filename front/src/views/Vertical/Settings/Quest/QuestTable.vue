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
      :on-close-editor="onCloseEditor">
      <template v-slot:editor>
        <div class="modal-row">
          <span class="w-20 mr-4">Name:</span>
          <input class="w-1/2 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
        </div>
        <div class="modal-row">
          <span class="w-20 mr-4">Category:</span>
          <select-dropdown
            class="h-10 w-64"
            :options-width-class="'w-64'"
            :state="category"
            :on-get="onGetCategory"
            :on-get-to-options="onGetCategoryToOptions"></select-dropdown>
        </div>
        <div class="modal-row" v-if="category.title">
          <span class="w-20 mr-4">Quest Id:</span>
          <select-dropdown
            class="h-10 w-64"
            :options-width-class="'w-64'"
            :state="quest"
            :on-get="onGetQuest"
            :on-get-to-options="onGetQuestToOptions"></select-dropdown>
          <ripple-button class="ml-2 btn btn-primary" @click="openQuestPage"> Add </ripple-button>
        </div>
        <div class="modal-row h-10" v-else></div>
        <div class="modal-row" v-if="category.title">
          <span class="w-20 mr-4">Priority:</span>
          <input
            class="w-1/2 modal-input"
            type="text"
            :placeholder="table.row.priority as any"
            v-model="table.row.priority" />
        </div>
        <div class="modal-row h-10" v-else></div>
      </template>
    </crud-table>
  </div>
</template>

<script lang="ts">
import { reactive, watch } from "vue";
import { useRouter } from "vue-router";

import { userState } from "@/state/user";

import { getDatetime } from "@/utils/datetime";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown, {
  SelectDropdownGetParam,
  SelectDropdownState,
  reset,
} from "@/elements/Dropdown/SelectDropdown.vue";
import CrudTable, { CrudTableState, Header } from "@/elements/Table/CrudTable/index.vue";

import { getUserElasticCountQuest, getUserElasticCountQuests } from "@/api/v1/user/quest/elasticCountQuest";

import {
  deleteUserQuest,
  getUserQuestTotal,
  getUserQuests,
  postUserQuest,
  putUserQuest,
} from "@/api/v1/user/quest/quest";

import { getSettingUserQuestCategories } from "@/api/v1/setting/userQuestCategory";

export interface Row {
  id?: number;
  user_id?: number;
  name: string;
  category_id: number;
  quest_id: number;
  priority: number;
  created?: string;
  modified?: string;
}

export default {
  components: { CrudTable, RippleButton, SelectDropdown },

  setup() {
    const router = useRouter();

    const userID = userState.id;
    const table = CrudTable.initState() as CrudTableState<Row>;

    const state = reactive({
      questUrl: undefined,
      onGetQuest: undefined,
    });

    const category = SelectDropdown.initState() as SelectDropdownState;
    function onGetCategory(params: SelectDropdownGetParam) {
      return getSettingUserQuestCategories(params);
    }
    function onGetCategoryToOptions(data: { name: string | number; id: number }) {
      return { title: data.name, value: data.id };
    }

    const quest = SelectDropdown.initState() as SelectDropdownState;
    function onGetQuest(params: SelectDropdownGetParam) {
      return state.onGetQuest(params);
    }
    function onGetQuestToOptions(data: { name: string | number; id: number }) {
      return { title: data.name, value: data.id };
    }

    watch(
      () => category.title,
      () => {
        state.questUrl = undefined;
        quest.options = [];
        if (category.title) {
          const categoryId = category.selectedValue as number;
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
      },
    );

    watch(
      () => {
        if (table.row) {
          return table.row.category_id;
        }
        return false;
      },
      () => {
        const categoryID = table.row.category_id;
        category.selectedValue = categoryID;
        category.title = getCategoryName(categoryID);
      },
    );

    watch(
      () => quest.title,
      () => {
        table.row.quest_id = quest.selectedValue as number;
      },
    );

    watch(
      () => {
        if (table.row) {
          return table.row.quest_id;
        }
        return false;
      },
      () => {
        const questID = table.row.quest_id;
        quest.selectedValue = questID;
        if (questID) {
          getUserElasticCountQuest(userID, questID).then((response) => {
            const data = response.data;
            if (data) {
              quest.title = data.name;
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
      reset(category);
      reset(quest);
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

    return {
      table,
      headers,
      category,
      onGetCategory,
      onGetCategoryToOptions,
      quest,
      onGetQuest,
      onGetQuestToOptions,
      openQuestPage,
      onCrudCreate,
      onCrudGet,
      onCrudGetTotal,
      onCrudUpdate,
      onCrudDelete,
      onCloseEditor,
    };
  },
};
</script>
