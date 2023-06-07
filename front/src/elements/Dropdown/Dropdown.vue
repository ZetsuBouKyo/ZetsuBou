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

<script lang="ts">
import { defineComponent, PropType, reactive, watch, getCurrentInstance, onBeforeMount } from "vue";

export enum Origin {
  BottomLeft,
  BottomRight,
}

export interface DropdownState {
  popout: boolean;
}

export interface OnClick {
  (): void;
}

export interface OnOpen {
  (): void;
}

export interface OnClose {
  (): void;
}

export interface DropdownStates {
  [key: string]: {
    close: () => void;
    group?: string;
  };
}

let dropdownStates: DropdownStates = {};

export default defineComponent({
  props: {
    state: {
      type: Object as PropType<DropdownState>,
      default: () => {
        return reactive<DropdownState>({ popout: false });
      },
    },
    origin: {
      type: Object as PropType<Origin>,
      default: Origin.BottomRight,
    },
    group: {
      type: Object as PropType<string>,
      default: undefined,
    },
    isExpand: {
      type: Object as PropType<boolean>,
      default: true,
    },
    isToggle: {
      type: Object as PropType<boolean>,
      default: true,
    },
    selectClass: {
      type: Object as PropType<string>,
      default: "border-r-2 border-gray-700",
    },
    optionsClass: {
      type: Object as PropType<string>,
      default: "",
    },
    optionsWidthClass: {
      type: Object as PropType<string>,
      default: "w-60",
    },
    optionsBgColorClass: {
      type: Object as PropType<string>,
      default: "bg-gray-800",
    },
    optionsOverflowYClass: {
      type: Object as PropType<string>,
      default: "overflow-y-auto",
    },
    optionsTopClass: {
      type: Object as PropType<string>,
      default: "top-2",
    },
    onClick: {
      type: Object as PropType<OnClick>,
      default: undefined,
    },
    onOpen: {
      type: Object as PropType<OnOpen>,
      default: undefined,
    },
    onClose: {
      type: Object as PropType<OnClose>,
      default: undefined,
    },
  },
  setup(props, { slots }) {
    const uid = getCurrentInstance().uid;
    let state = props.state;
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
    }

    function open() {
      state.popout = true;
    }

    function close() {
      state.popout = false;
    }

    watch(
      () => state.popout,
      () => {
        if (state.popout) {
          if (props.onOpen) {
            props.onOpen();
          }
          for (let key in dropdownStates) {
            if (props.group === undefined) {
              dropdownStates[key].close();
              delete dropdownStates[key];
            } else if (props.group === dropdownStates[key].group) {
              dropdownStates[key].close();
              delete dropdownStates[key];
            }
          }
          dropdownStates[uid] = { group: props.group, close: close };
        } else {
          if (props.onClose !== undefined) {
            props.onClose();
          }
          delete dropdownStates[uid];
        }
      },
    );

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

    return { ...props, Origin, _optionsClass, isSelect, selectToggle, expandToggle, open, close, toggle };
  },
});
</script>
