<script setup lang="ts">
import { PropType, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import {
    SelectDropdownMode,
    SelectDropdownOnGet,
    SelectDropdownState,
} from "@/elements/Dropdown/SelectDropdown.interface";
import { SearchCategory } from "@/interface/search";
import { Source } from "@/interface/source";
import { DataState } from "@/interface/state";
import { TagFieldsPrivateState, Token } from "@/interface/tag";
import {
    AdvancedSearchField,
    AdvancedSearchFieldKeyEnum,
    AdvancedSearchFieldType,
    AdvancedSearchState,
} from "./interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";
import Modal from "@/elements/Modal/Modal.vue";

import {
    getSettingFrontGalleryStartsWithCategories,
    getSettingFrontGalleryStartsWithTagFields,
} from "@/api/v1/setting/front/gallery";
import {
    getSettingFrontVideoStartsWithCategories,
    getSettingFrontVideoStartsWithTagFields,
} from "@/api/v1/setting/front/video";
import { getTagTokenStartsWith } from "@/api/v1/tag/token";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";
import { settingState } from "@/state/Setting/front";

import { durationToSecond, secondToDuration } from "@/utils/datetime";
import { watchLabels, watchLabelsChipsLength } from "@/utils/label";
import { detectRouteChange } from "@/utils/route";
import { toTitle } from "@/utils/str";
import { onGetTip, onMouseoverOption, watchTagFieldsChipsLength, watchTags } from "@/utils/tag";
import { RouteQueryKey } from "./field";

const props = defineProps({
    state: {
        type: Object as PropType<AdvancedSearchState>,
        required: true,
    },
});

const advancedSearch = ref();
const route = useRoute();
const router = useRouter();
const state = props.state;

// Should not be changed directly.
const privateState = reactive<TagFieldsPrivateState>({
    tagFields: {},
    onGets: {},
});

// If we want to change the UI of tags or labels, we should update this.
const sourceState = reactive<DataState<Source>>({
    data: { labels: [], tags: {} },
});

const labels = initSelectDropdownState() as SelectDropdownState;
watch(...watchLabels(labels, sourceState));
watch(...watchLabelsChipsLength(labels, sourceState));

const tagFields = initSelectDropdownState() as SelectDropdownState;
watch(...watchTags(privateState, tagFields, sourceState));
watch(...watchTagFieldsChipsLength(privateState, tagFields, sourceState));

const categories = initSelectDropdownState() as SelectDropdownState;
const onGetCategoriesToOptions = tokenToOption;

const uploader = initSelectDropdownState() as SelectDropdownState;
const onGetUploader = getTagTokenStartsWith;
const onGetUploaderToOptions = tokenToOption;

function resetCategoryAndUploader() {
    categories.title = undefined;
    uploader.title = undefined;
}

function resetSourceState() {
    sourceState.data.labels = [];
    sourceState.data.tags = {};
}

function resetFieldValues() {
    for (const field of state.fields) {
        field.value = undefined;
        switch (field.type) {
            case AdvancedSearchFieldType.String:
                field.fuzziness.title = undefined;
                field.fuzziness.selectedValue = undefined;

                field.analyzer.title = undefined;
                field.analyzer.selectedValue = undefined;

                field.boolean.title = undefined;
                field.boolean.selectedValue = undefined;

                break;
            case AdvancedSearchFieldType.Duration:
            case AdvancedSearchFieldType.Range:
                field.gte = undefined;
                field.lte = undefined;
                break;
        }
    }
}

// Update the default labels by `route'.
function loadLabels() {
    const keys = Object.keys(route.query);
    for (const key of keys) {
        if (key.startsWith("label_")) {
            sourceState.data.labels.push(route.query[key].toString());
        }
    }
}

// Update the default tags by `route`.
function loadTags() {
    const pattern = /tag_field_(\d+)/;
    const keys = Object.keys(route.query);
    for (const key of keys) {
        const match = key.match(pattern);
        if (match === null) {
            continue;
        }

        const tagField = route.query[key].toString();
        if (!sourceState.data.tags.hasOwnProperty(tagField)) {
            sourceState.data.tags[tagField] = [];
        }

        const index = match[1];
        const tagValueKey = `tag_value_${index}`;
        const tagValue = route.query[tagValueKey] as string;
        if (tagValue === undefined) {
            continue;
        }
        sourceState.data.tags[tagField].push(tagValue);
    }
}

function loadFieldValue(field: AdvancedSearchField) {
    const name = field.name;
    if (!name) {
        return;
    }
    if (route.query[name]) {
        field.value = route.query[name] as string;
    }
}

// Update the default value of the fields by `route`.
function loadFieldValues() {
    for (const field of state.fields) {
        loadFieldValue(field);

        const routeKey = new RouteQueryKey(field.name);
        let gte: any;
        let lte: any;
        switch (field.type) {
            case AdvancedSearchFieldType.String:
                const fuzziness = Number(route.query[routeKey.fuzziness]);
                field.fuzziness.title = undefined;
                field.fuzziness.selectedValue = undefined;
                if (!Number.isNaN(fuzziness)) {
                    field.fuzziness.title = fuzziness;
                    field.fuzziness.selectedValue = fuzziness;
                }

                const analyzer = route.query[routeKey.analyzer] as string;
                field.analyzer.title = undefined;
                field.analyzer.selectedValue = undefined;
                if (analyzer) {
                    field.analyzer.title = toTitle(analyzer);
                    field.analyzer.selectedValue = analyzer;
                }

                const bool = route.query[routeKey.bool] as string;
                field.boolean.title = undefined;
                field.boolean.selectedValue = undefined;
                if (bool) {
                    field.boolean.title = toTitle(bool);
                    field.boolean.selectedValue = bool;
                }
                break;
            case AdvancedSearchFieldType.Duration:
                gte = Number(route.query[routeKey.gte]);
                field.gte = undefined;
                if (!Number.isNaN(gte)) {
                    field.gte = secondToDuration(gte);
                }

                lte = Number(route.query[routeKey.lte]);
                field.lte = undefined;
                if (!Number.isNaN(lte)) {
                    field.lte = secondToDuration(lte);
                }
                break;
            case AdvancedSearchFieldType.Range:
                gte = Number(route.query[routeKey.gte]);
                field.gte = undefined;
                if (!Number.isNaN(gte)) {
                    field.gte = gte;
                }

                lte = Number(route.query[routeKey.lte]);
                field.lte = undefined;
                if (!Number.isNaN(lte)) {
                    field.lte = lte;
                }
                break;
        }
    }
}

function loadCategoryAndUploader() {
    const c = route.query.category as string;
    if (c) {
        categories.title = c;
    }
    const u = route.query.uploader as string;
    if (u) {
        uploader.title = u;
    }
}

// Update the fields by the `props.state` and `settingState`.
function initSubFields() {
    for (const field of state.fields) {
        switch (field.type) {
            case AdvancedSearchFieldType.String:
                field.fuzziness = initSelectDropdownState() as SelectDropdownState;
                field.fuzziness.options = [
                    { title: 0, value: 0 },
                    { title: 1, value: 1 },
                    { title: 2, value: 2 },
                    { title: 3, value: 3 },
                ];

                field.analyzer = initSelectDropdownState() as SelectDropdownState;

                let analyzers: any;

                switch (field.keyType) {
                    case AdvancedSearchFieldKeyEnum.BuiltIn:
                        analyzers = settingState.data[state.category].analyzer.keyword as object;
                        for (let analyzer in analyzers) {
                            field.analyzer.options.push({ title: toTitle(analyzer), value: analyzer });
                        }
                        break;
                    case AdvancedSearchFieldKeyEnum.ElasticsearchField:
                        analyzers = settingState.data[state.category].analyzer.field[field.key] as Array<string>;
                        for (let analyzer of analyzers) {
                            field.analyzer.options.push({ title: toTitle(analyzer), value: analyzer });
                        }
                        break;
                }

                field.boolean = initSelectDropdownState() as SelectDropdownState;
                field.boolean.options = [
                    { title: "Should", value: "should" },
                    { title: "Must", value: "must" },
                ];
                break;
        }
    }
}

function load() {
    if (settingState.data === undefined) {
        return;
    }
    initSubFields();

    loadCategoryAndUploader();
    loadFieldValues();
    loadLabels();
    loadTags();
}
load();

watch(
    () => detectRouteChange(route),
    () => {
        if (route.path.endsWith("advanced-search")) {
            load();
        } else {
            reset();
        }
    },
);

let onGetCategories: SelectDropdownOnGet<Token>;
let getStartsWithTagFields: SelectDropdownOnGet<Token>;
switch (state.category) {
    case SearchCategory.Gallery:
        onGetCategories = getSettingFrontGalleryStartsWithCategories;
        getStartsWithTagFields = getSettingFrontGalleryStartsWithTagFields;
        break;
    case SearchCategory.Video:
        onGetCategories = getSettingFrontVideoStartsWithCategories;
        getStartsWithTagFields = getSettingFrontVideoStartsWithTagFields;
}

function search() {
    const queries = {};

    if (categories.title !== undefined) {
        queries["category"] = categories.title;
    }

    if (uploader.title !== undefined) {
        queries["uploader"] = uploader.title;
    }

    for (const field of state.fields) {
        if (field.name === undefined) {
            continue;
        }

        const routeKey = new RouteQueryKey(field.name);
        switch (field.type) {
            case AdvancedSearchFieldType.String:
                if (field.value === undefined) {
                    break;
                }
                queries[field.name] = field.value;

                if (field.fuzziness.selectedValue !== undefined && Number.isInteger(field.fuzziness.selectedValue)) {
                    queries[routeKey.fuzziness] = field.fuzziness.selectedValue;
                }
                if (field.analyzer.selectedValue != undefined) {
                    queries[routeKey.analyzer] = field.analyzer.selectedValue;
                }
                if (field.boolean.selectedValue != undefined) {
                    queries[routeKey.bool] = field.boolean.selectedValue;
                }
                break;
            case AdvancedSearchFieldType.Range:
                if (field.gte !== undefined && !Number.isNaN(Number(field.gte as string))) {
                    queries[routeKey.gte] = field.gte;
                }
                if (field.lte !== undefined && !Number.isNaN(Number(field.lte as string))) {
                    queries[routeKey.lte] = field.lte;
                }
                break;
            case AdvancedSearchFieldType.Duration:
                if (field.gte !== undefined) {
                    if (!Number.isNaN(Number(field.gte as string))) {
                        queries[routeKey.gte] = field.gte;
                    } else {
                        const gte = durationToSecond(field.gte as string);
                        if (!Number.isNaN(gte)) {
                            queries[routeKey.gte] = gte;
                        }
                    }
                }
                if (field.lte !== undefined) {
                    if (!Number.isNaN(Number(field.lte as string))) {
                        queries[routeKey.lte] = field.lte;
                    } else {
                        const lte = durationToSecond(field.lte as string);
                        if (!Number.isNaN(lte)) {
                            queries[routeKey.lte] = lte;
                        }
                    }
                }
                break;
        }
    }

    let k = 1;
    for (let i = 0; i < labels.chips.length; i++) {
        const chip = labels.chips[i];
        if (chip.title !== undefined) {
            queries[`label_${k}`] = chip.title;
            k++;
        }
    }

    k = 1;
    for (let tagField in sourceState.data.tags) {
        const chips = privateState.tagFields[tagField].chips;
        for (const chip of chips) {
            queries[`tag_field_${k}`] = tagField;
            queries[`tag_value_${k}`] = chip.title;
            k++;
        }
    }

    const queriesArray = [];
    for (const key in queries) {
        queriesArray.push(`${key}=${queries[key]}`);
    }

    const queriesStr = queriesArray.join("&");
    const url = `/${state.category}/advanced-search?${queriesStr}`;

    window.scrollTo(0, 0);
    router.push(url);
    advancedSearch.value.close();
}

function reset() {
    resetCategoryAndUploader();
    resetFieldValues();
    resetSourceState();
}

function open() {
    advancedSearch.value.open();
}

function tokenToOption(token: { id: number; name: string }) {
    return { title: token.name, value: token.id };
}

defineExpose({
    open,
    reset,
});
</script>

<template>
    <modal
        ref="advancedSearch"
        :title="'Advanced Search'"
        class="top-12 w-full lg:w-3/4 lg:left-1/8 2xl:w-1/2 2xl:left-1/4"
        :is-scrollable="true"
        :key="detectRouteChange(route)"
        @keyup.enter="search"
    >
        <div class="flex flex-col" v-for="(field, i) in state.fields" :key="i">
            <div class="flex flex-col" v-if="field.type === AdvancedSearchFieldType.String">
                <div class="modal-row h-10">
                    <span class="w-28 mr-4 text-white">{{ toTitle(field.name).replace("_", " ") }}:</span>
                    <input class="modal-input flex-1" type="text" :placeholder="field.value" v-model="field.value" />
                </div>
                <div class="modal-row h-10">
                    <span class="w-18 ml-auto mr-4">Fuzziness:</span>
                    <select-dropdown
                        class="w-20 mr-4"
                        :group="'search'"
                        :options-width-class="'w-20'"
                        :origin="Origin.BottomLeft"
                        :state="field.fuzziness"
                    />
                    <span class="w-16 mr-4">Analyzer:</span>
                    <select-dropdown
                        class="w-32 mr-4"
                        :group="'search'"
                        :options-width-class="'w-32'"
                        :origin="Origin.BottomLeft"
                        :state="field.analyzer"
                    />
                    <span class="w-16 mr-4">Boolean:</span>
                    <select-dropdown
                        class="w-28"
                        :group="'search'"
                        :options-width-class="'w-28'"
                        :origin="Origin.BottomLeft"
                        :state="field.boolean"
                    />
                </div>
            </div>
            <div class="flex flex-col" v-else-if="field.type === AdvancedSearchFieldType.Range">
                <div class="modal-row h-10">
                    <span class="w-28 mr-4 text-white">{{ toTitle(field.name) }}:</span>
                    <input
                        class="modal-input flex-1 w-24 sm:w-full"
                        type="text"
                        :placeholder="field.gte as string"
                        v-model="field.gte"
                    />
                    <span class="mx-4">to</span>
                    <input
                        class="modal-input flex-1 w-24 sm:w-full"
                        type="text"
                        :placeholder="field.lte as string"
                        v-model="field.lte"
                    />
                </div>
            </div>
            <div class="flex flex-col" v-else-if="field.type === AdvancedSearchFieldType.Duration">
                <div class="modal-row h-10">
                    <span class="w-28 mr-4 text-white">{{ toTitle(field.name) }}:</span>
                    <input
                        class="modal-input flex-1 w-24 sm:w-full"
                        type="text"
                        placeholder="e.g. hh:mm:ss, mm:ss, or ss"
                        v-model="field.gte"
                    />
                    <span class="mx-4">to</span>
                    <input
                        class="modal-input flex-1 w-24 sm:w-full"
                        type="text"
                        placeholder="e.g. hh:mm:ss, mm:ss, or ss"
                        v-model="field.lte"
                    />
                </div>
            </div>
        </div>
        <div class="modal-row h-10">
            <span class="w-28 mr-4 text-white">Category:</span>
            <select-dropdown
                class="flex-1"
                :options-width-class="'w-96'"
                :origin="Origin.BottomLeft"
                :state="categories"
                :is-auto-complete="true"
                :on-get="onGetCategories"
                :on-get-to-options="onGetCategoriesToOptions"
                :on-get-tip="onGetTip"
                :on-mouseover-option="onMouseoverOption"
                :mode="SelectDropdownMode.Input"
            />
        </div>
        <div class="modal-row h-10">
            <span class="w-28 mr-4 text-white">Uploader:</span>
            <select-dropdown
                class="flex-1"
                :options-width-class="'w-96'"
                :origin="Origin.BottomLeft"
                :state="uploader"
                :is-auto-complete="true"
                :on-get="onGetUploader"
                :on-get-to-options="onGetUploaderToOptions"
                :on-get-tip="onGetTip"
                :on-mouseover-option="onMouseoverOption"
                :mode="SelectDropdownMode.Input"
            />
        </div>
        <div class="modal-row" @keyup.enter.stop="">
            <span class="w-28 mr-4 text-white">Labels:</span>
            <select-dropdown
                class="flex-1"
                :is-input-chips-title-unique="true"
                :options-width-class="'w-64'"
                :origin="Origin.BottomLeft"
                :state="labels"
                :on-get="getTagTokenStartsWith"
                :on-get-to-options="tokenToOption"
                :mode="SelectDropdownMode.InputChips"
            />
        </div>
        <div class="modal-row" @keyup.enter.stop="">
            <span class="w-28 mr-4 text-white">Tag Fields:</span>
            <select-dropdown
                class="flex-1"
                :is-input-chips-title-unique="true"
                :options-width-class="'w-64'"
                :origin="Origin.BottomLeft"
                :state="tagFields"
                :on-get="getStartsWithTagFields"
                :on-get-to-options="tokenToOption"
                :mode="SelectDropdownMode.InputChips"
            />
        </div>
        <div class="modal-row" v-for="(_, field) in privateState.tagFields" :key="field" @keyup.enter.stop="">
            <span class="w-28 mx-4">{{ field }}:</span>
            <select-dropdown
                class="flex-1"
                :is-input-chips-title-unique="true"
                :options-width-class="'w-64'"
                :origin="Origin.BottomLeft"
                :state="privateState.tagFields[field]"
                :on-get="privateState.onGets[field]"
                :on-get-to-options="tokenToOption"
                :mode="SelectDropdownMode.InputChips"
            />
        </div>
        <div class="modal-row">
            <div class="flex ml-auto">
                <ripple-button class="flex btn btn-primary" @click="search"> Search </ripple-button>
            </div>
        </div>
    </modal>
</template>
