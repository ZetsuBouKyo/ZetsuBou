<template>
  <li class="ml-4 my-4">
    <svg
      class="absolute w-6 h-6 mt-3 -left-3 bg-gray-800"
      xmlns="http://www.w3.org/2000/svg"
      width="256"
      height="256"
      viewBox="2 2 20 20"
      style="font-size: 1.4rem"
      v-if="state.ok">
      <path
        fill="rgb(96,165,250)"
        d="m10 17l-5-5l1.41-1.42L10 14.17l7.59-7.59L19 8m-7-6A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10A10 10 0 0 0 12 2Z" />
    </svg>
    <icon-mdi-circle
      class="absolute w-6 h-6 mt-3 -left-3 bg-gray-800"
      width="256"
      height="256"
      viewBox="2 2 20 20"
      style="font-size: 1.4rem"
      v-else />
    <div class="flex flex-col px-4 pt-3">
      <span class="text text-white text-lg">Step {{ state.index + 1 }}. {{ state.title }}</span>
      <div
        class="flex flex-col bg-gray-900 shadow-gray-900 rounded-lg scrollbar-gray-900-2 p-8 my-4 animate-fade-in"
        v-if="!state.close">
        <div class="flex flex-col w-full">
          <slot name="body"></slot>
          <div class="flex flex-row mt-2">
            <div class="flex flex-row ml-auto">
              <slot name="buttons"></slot>
              <ripple-button
                class="flex btn btn-primary ml-2 disabled:bg-gray-400"
                @click="previous(state)"
                v-if="state.index > 0">
                Previous
              </ripple-button>
              <ripple-button
                class="flex btn btn-primary ml-2 disabled:bg-gray-400"
                @click="next(state)"
                :disabled="!state.next"
                v-if="state.index < state.steps.length - 1">
                Next
              </ripple-button>
              <ripple-button class="flex btn btn-primary ml-2 disabled:bg-gray-400" @click="finish(state)" v-else>
                Finish
              </ripple-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </li>
</template>

<script lang="ts">
import { PropType, reactive } from "vue";

import { Setting } from "@/interface/setting";

import RippleButton from "@/elements/Button/RippleButton.vue";

export interface StepState {
  index: number;
  title: string;
  ok: boolean;
  close: boolean;
  next: boolean;
  setting?: Setting;
  steps?: Array<StepState>;
  [key: string]: any;
}

export interface OnFinish {
  (state: StepState): void;
}

export function initStepState(index: number, title: string, close: boolean) {
  return reactive<StepState>({ index: index, title: title, ok: false, close: close, ports: undefined, next: false });
}

export default {
  components: { RippleButton },
  props: {
    state: {
      type: Object as PropType<StepState>,
      default: initStepState(0, "", false),
    },
    onFinish: {
      type: Object as PropType<OnFinish>,
      default: undefined,
    },
  },
  setup(props) {
    const state = props.state;

    function previous(state: StepState) {
      if (state.index > 0) {
        state.close = true;
        const previousIndex = state.index - 1;
        const previousStep = state.steps[previousIndex];
        previousStep.close = false;
      }
    }

    function next(state: StepState) {
      state.ok = true;
      state.close = true;
      const nextIndex = state.index + 1;
      if (state.steps && nextIndex < state.steps.length) {
        state.steps[nextIndex].close = false;
      }
    }

    function finish(state: StepState) {
      if (props.onFinish !== undefined) {
        props.onFinish(state);
      }
    }

    return { state, previous, next, finish };
  },
};
</script>
