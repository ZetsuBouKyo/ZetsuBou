<script setup lang="ts">
import { getCurrentInstance, onBeforeMount, reactive, useSlots } from "vue";

import { DropdownState, OnClick, OnClose, OnOpen, Origin } from "./Dropdown.interface";

import { dropdownsState } from "@/state/dropdown";

interface Props {
    origin: Origin;
    group: string;
    isExpand: boolean;
    isToggle: boolean;
    selectClass: string;
    optionsClass: string;
    optionsWidthClass: string;
    optionsBgColorClass: string;
    optionsOverflowYClass: string;
    optionsTopClass: string;
    onClick: OnClick;
    onOpen: OnOpen;
    onClose: OnClose;
}

const props = withDefaults(defineProps<Props>(), {
    origin: Origin.BottomRight,
    group: undefined,
    isExpand: true,
    isToggle: true,
    selectClass: "border-r-2 border-gray-700",
    optionsClass: "",
    optionsWidthClass: "w-60",
    optionsBgColorClass: "bg-gray-800",
    optionsOverflowYClass: "overflow-y-auto",
    optionsTopClass: "top-2",
    onClick: undefined,
    onOpen: undefined,
    onClose: undefined,
});

const uid: string = getCurrentInstance().uid.toString();
const state = reactive<DropdownState>({ popout: false }) as DropdownState;

const slots = useSlots();
const isSelect = slots.select !== undefined;

function selectToggle() {
    if (props.isExpand) {
        return;
    }
    expandToggle();
}

function expandToggle() {
    if (!props.isToggle) {
        return;
    }
    toggle();
}

function toggle() {
    state.popout = !state.popout;
    update();
}

function open() {
    state.popout = true;
    update();
}

function close() {
    state.popout = false;
    update();
}

function update() {
    if (state.popout) {
        if (props.onOpen) {
            props.onOpen();
        }
        for (let key in dropdownsState.data) {
            if (key === uid) {
                continue;
            }
            if (props.group === undefined) {
                dropdownsState.data[key].close();
                dropdownsState.delete(key);
            } else if (dropdownsState.data[key] && props.group === dropdownsState.data[key].group) {
                dropdownsState.data[key].close();
                dropdownsState.delete(key);
            }
        }
        dropdownsState.add(uid, { group: props.group, close: close });
    } else {
        if (props.onClose !== undefined) {
            props.onClose();
        }
        dropdownsState.delete(uid);
    }
}

onBeforeMount(() => {
    document.addEventListener.call(window, "click", () => {
        close();
    });
});

function getOptionsClass() {
    const optionsClasses: Array<string> = [];
    const optionsClassKeys = Object.keys(props);
    for (const key of optionsClassKeys) {
        if (key.startsWith("options") && key.endsWith("Class") && typeof props[key] === "string") {
            optionsClasses.push(props[key]);
        }
    }

    if (props.origin === Origin.BottomLeft) {
        optionsClasses.push("left-0");
    } else {
        optionsClasses.push("right-0");
    }

    const tempOptionsClass = props.optionsClass.split(" ");
    for (const key of tempOptionsClass) {
        if (!optionsClasses.includes(key)) {
            optionsClasses.push(key);
        }
    }

    return optionsClasses.join(" ");
}

const _optionsClass = getOptionsClass();

defineExpose({ open, toggle, close });
</script>

<template>
    <div class="relative h-full w-full">
        <div class="relative h-full w-full inline-flex items-center focus:outline-none cursor-default">
            <div class="h-full focus:outline-none" :class="isSelect ? selectClass : ''" @click.stop="selectToggle">
                <slot name="select"></slot>
            </div>
            <div
                class="h-full flex flex-col justify-center hover:opacity-50 cursor-pointer"
                v-if="isExpand"
                @click.stop="expandToggle"
            >
                <icon-ic-round-expand-more class="mx-1" />
            </div>
        </div>
        <div class="absolute bottom-0" :class="origin === Origin.BottomLeft ? 'left-0' : 'right-0'">
            <div
                class="scrollbar-gray-900-2 absolute ring-1 ring-black ring-opacity-5 focus:outline-none text-base text-white 3xl:text-lg shadow-black rounded z-40"
                :class="_optionsClass"
                @click.stop="onClick"
                v-if="state.popout"
            >
                <slot name="options"></slot>
            </div>
        </div>
    </div>
</template>
