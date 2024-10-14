<script setup lang="ts">
import { reactive, ref, watch } from "vue";

import { DropdownOnOpen, Origin } from "./Dropdown.interface";
import {
    SelectDropdownOnGetTip,
    SelectDropdownOnInput,
    SelectDropdownOnMouseoverOption,
    SelectDropdownOnScroll,
    SelectDropdownOnSelect,
    SelectDropdownOption,
    SelectDropdownScroll,
} from "./SelectDropdown.interface";

import BaseSelectDropdown from "./BaseSelectDropdown.vue";

interface State {
    scroll: SelectDropdownScroll;
    lock: boolean;
    isFocus: boolean;
}

interface Props {
    group: string;
    origin: Origin;
    isAutoCompleteOptionCaseSensitive: boolean;
    isAutoComplete: boolean;
    widthClass: string;
    optionsWidthClass: string;
    onInput: SelectDropdownOnInput;
    onOpen: DropdownOnOpen;
    onScroll: SelectDropdownOnScroll;
    onSelect: SelectDropdownOnSelect;
    onGetTip: SelectDropdownOnGetTip;
    onMouseoverOption: SelectDropdownOnMouseoverOption;
}

const props = withDefaults(defineProps<Props>(), {
    group: undefined,
    origin: Origin.BottomRight,
    isAutoCompleteOptionCaseSensitive: false,
    isAutoComplete: true,
    widthClass: "",
    optionsWidthClass: "w-60",
    onInput: undefined,
    onOpen: undefined,
    onScroll: undefined,
    onSelect: undefined,
    onGetTip: undefined,
    onMouseoverOption: undefined,
});

const title = defineModel<string | string[] | number>("title", { default: "" });
const selectedValue = defineModel<any>("selectedValue", { default: undefined });
const defaultOptions = defineModel<Array<SelectDropdownOption>>("defaultOptions", { default: [] });
let options = defineModel<Array<SelectDropdownOption>>("options", { default: [] });
const scrollEnd = defineModel<boolean>("scrollEnd", { default: false });

const baseSelectDropdown = ref();

const state = reactive<State>({
    scroll: { isEnd: false },
    lock: false,
    isFocus: false,
});

function select(opt: SelectDropdownOption) {
    title.value = opt.title;
    selectedValue.value = opt.value;

    if (props.onSelect) {
        props.onSelect(opt);
    }
}

function focusOpenDropdown() {
    state.isFocus = true;
    baseSelectDropdown.value.toggle();
}

function toggleDropdown() {
    if (state.isFocus) {
        state.isFocus = false;
        return;
    }
    baseSelectDropdown.value.toggle();
}

function updateOptions(title: string) {
    props.onInput(title);
}

function updateOptionsWithDefaultOptions(title: string) {
    if (!defaultOptions.value || defaultOptions.value.length === 0) {
        return;
    }

    // We cannot simply use `options.value = []` here.
    while (options?.value.length) {
        options.value.pop();
    }
    for (let option of defaultOptions.value) {
        option = JSON.parse(JSON.stringify(option));
        let optionTitle = option.title as string;
        let stateTitle = title as string;
        if (!props.isAutoCompleteOptionCaseSensitive) {
            optionTitle = optionTitle.toLowerCase();
            stateTitle = title.toString().toLowerCase();
        }
        if (optionTitle.startsWith(stateTitle)) {
            options.value.push(option);
        }
    }
}

function updateInput() {
    const text = title.value as string;
    if (!props.isAutoComplete) {
        return;
    }

    if (props.onInput !== undefined) {
        updateOptions(text);
    } else {
        updateOptionsWithDefaultOptions(text);
    }
    baseSelectDropdown.value.open();
}

function open() {
    baseSelectDropdown.value.open();
}

function close() {
    baseSelectDropdown.value.close();
}

function toggle() {
    baseSelectDropdown.value.toggle();
}

function clear() {
    title.value = "";
    selectedValue.value = undefined;
}

defineExpose({ open, close, toggle, clear });
</script>

<template>
    <base-select-dropdown
        ref="baseSelectDropdown"
        v-model:options="options"
        v-model:scroll-end="scrollEnd"
        :group="group"
        :origin="origin"
        :width-class="widthClass"
        :options-width-class="optionsWidthClass"
        :on-open="onOpen"
        :on-scroll="onScroll"
        :on-select="select"
        :on-get-tip="onGetTip"
        :on-mouseover-option="onMouseoverOption"
    >
        <template v-slot:select>
            <div class="relative h-full w-full inline-flex items-center">
                <input
                    class="w-full modal-input"
                    type="search"
                    :placeholder="title as string"
                    v-model="title"
                    @click.stop="toggleDropdown"
                    @focus="focusOpenDropdown"
                    @input="updateInput"
                />
                <icon-ic-round-expand-more class="absolute text-white right-0 ml-2 mr-3" style="font-size: 1rem" />
            </div>
        </template>
    </base-select-dropdown>
</template>
