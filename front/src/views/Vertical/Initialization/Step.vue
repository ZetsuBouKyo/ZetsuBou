<script setup lang="ts">
import { OnFinish, StepState } from "./Step.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";

import { initStepState } from "./Step";

interface Props {
  state: StepState;
  onFinish: OnFinish;
}
const props = withDefaults(defineProps<Props>(), {
  state: () => initStepState(0, "", false),
  onFinish: undefined,
});

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
</script>

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
