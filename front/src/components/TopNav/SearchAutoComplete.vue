<script setup lang="ts">
import { AxiosResponse } from "axios";
import { PropType, reactive, watch } from "vue";

import { SearchCategory, SearchState } from "@/interface/search";
import { Token } from "@/interface/tag";

import { getGalleryFieldNames, getVideoFieldNames } from "@/api/v1/elasticsearch";
import { getTagTokenStartsWith } from "@/api/v1/tag/token";

enum SearchAutoCompleteOptionEnum {
    Command = "Command",
    Text = "Text",
}

export interface SearchAutoCompleteOptionOnClick {
    (): void;
}

interface SearchAutoCompleteOption {
    category: SearchAutoCompleteOptionEnum;
    value: string;
    onClick: SearchAutoCompleteOptionOnClick;
}

interface SearchAutoCompleteState {
    category: SearchCategory.Gallery;
    popout: boolean;
    width: number;
    options: Array<SearchAutoCompleteOption>;
    fieldNames: Array<string>;
    getFieldNames: () => Promise<AxiosResponse<Array<string>>>;
}

const valueSep = "=";
const props = defineProps({
    searchState: {
        type: Object as PropType<SearchState>,
        required: true,
    },
    width: {
        type: Object as PropType<number>,
        required: true,
    },
});

const searchState = props.searchState;
const state = reactive<SearchAutoCompleteState>({
    category: undefined,
    popout: false,
    width: undefined,
    options: [],
    fieldNames: [],
    getFieldNames: undefined,
});

state.width = props.width;

watch(
    () => props.width,
    () => {
        state.width = props.width;
    },
);

function updateFieldNames() {
    if (props.searchState?.category !== undefined) {
        state.category = props.searchState.category as any;
        switch (state.category) {
            case SearchCategory.Gallery:
                state.getFieldNames = getGalleryFieldNames;
                break;
            case SearchCategory.Video:
                state.getFieldNames = getVideoFieldNames;
                break;
        }
        state.getFieldNames().then((response: any) => {
            if (response.data) {
                state.fieldNames = response.data;
            } else {
                state.fieldNames = [];
            }
        });
    }
}
watch(
    () => props.searchState?.category,
    () => {
        updateFieldNames();
    },
);
updateFieldNames();

function getS(keyword: string) {
    if (!keyword) {
        return keyword;
    }

    const i = keyword.indexOf(valueSep);

    keyword = keyword.slice(i + 1);
    return keyword;
}

function updateOptionsWithFieldNames(keywords: Array<string>, keyword: string) {
    const i = keyword.indexOf(valueSep);
    if (i !== -1 || !keyword) {
        return;
    }

    const signIndex = keyword.indexOf("-");
    let k = keyword.toLowerCase();
    if (signIndex === 0) {
        k = keyword.slice(1);
        if (!k) {
            return;
        }
    }
    let c = 0;
    for (const fieldName of state.fieldNames) {
        if (c > 5) {
            return;
        }
        const fieldNameArray = fieldName.split(".");
        const lastFieldName = fieldNameArray.pop();
        const lastFieldNameLowerCase = lastFieldName.toLowerCase();
        if (!lastFieldName) {
            continue;
        }
        if (lastFieldNameLowerCase.startsWith(k)) {
            c += 1;
            state.options.push({
                category: SearchAutoCompleteOptionEnum.Command,
                value: fieldName,
                onClick: () => {
                    const valueSepIndex = keyword.indexOf(valueSep);
                    if (valueSepIndex !== -1) {
                        return;
                    }

                    let lastKeyword = fieldName;
                    if (signIndex === 0) {
                        lastKeyword = `-${lastKeyword}`;
                    }

                    keywords.push(lastKeyword);
                    searchState.query.keywords = keywords.join(" ");
                },
            });
        }
    }
}

function updateOptions(cur: string, pre: string) {
    state.options = [];
    if (!cur) {
        return;
    }

    const keywords = cur.split(" ");
    const keyword = keywords.pop();
    const s = getS(keyword);
    if (!s) {
        return;
    }
    getTagTokenStartsWith({ s: s, size: 5 }).then((response: any) => {
        let tokens: Array<Token> = response.data;
        tokens = Array.from(new Set(tokens));
        for (const token of tokens) {
            state.options.push({
                category: SearchAutoCompleteOptionEnum.Text,
                value: token.name,
                onClick: () => {
                    const i = keyword.indexOf(valueSep);
                    if (i === -1) {
                        keywords.push(token.name);
                    } else {
                        const fieldName = keyword.split(valueSep)[0];
                        let fieldValue = token.name;
                        if (token.name.includes(" ")) {
                            fieldValue = `"${fieldValue}"`;
                        }
                        const lastKeyword = `${fieldName}${valueSep}${fieldValue}`;
                        keywords.push(lastKeyword);
                    }
                    searchState.query.keywords = keywords.join(" ");
                },
            });
        }
        updateOptionsWithFieldNames(keywords, keyword);
    });
}
updateOptions(searchState.query.keywords, "");

watch(
    () => searchState.query.keywords,
    (cur, pre) => {
        updateOptions(cur, pre);
    },
);

function open() {
    state.popout = true;
}

function close() {
    state.popout = false;
}

function isOpened() {
    return state.popout && state.options.length > 0;
}

function click(option: SearchAutoCompleteOption) {
    option.onClick();
}

defineExpose({ open, close, isOpened });
</script>

<template>
    <div class="absolute bottom-0 left-0 flex flex-col">
        <div
            class="absolute flex flex-col bg-gray-700 rounded-b-lg py-2"
            :style="{ width: state.width + 'px' }"
            v-if="state.popout && state.options.length > 0 && searchState.query.keywords"
        >
            <!-- Be aware of click, mousedown and focusout -->
            <div class="flex flex-col max-h-80v overflow-y-scroll scrollbar-gray-900-2">
                <div
                    class="flex flex-col py-2 hover:bg-gray-500 hover:cursor-pointer border-l-4 border-gray-700 hover:border-blue-500"
                    v-for="(option, key) in state.options"
                    @mousedown="click(option)"
                    :key="key"
                    :tabindex="key"
                >
                    <div class="flex flex-col px-2 py-1">
                        <span class="text-xs text-white">{{ option.category }}</span>
                        <span class="text-base text-white">{{ option.value }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
