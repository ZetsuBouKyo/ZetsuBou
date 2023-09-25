<script setup lang="ts">
import { PropType } from "vue";

import { Source } from "@/interface/source";
import { SourceState } from "@/interface/state";

import RippleButton from "@/elements/Button/RippleButton.vue";

import { getValue } from "@/utils/obj";

const props = defineProps({
  state: {
    type: Object as PropType<SourceState<Source>>,
    required: true,
  },
  title: {
    type: Object as PropType<string>,
  },
  stateKey: {
    type: Object as PropType<string>,
  },
});

const stringArray = getValue(props.state, props.stateKey);

function addItem() {
  stringArray.push("");
}
function deleteItem(i: number) {
  stringArray.splice(i, 1);
}
</script>

<template>
  <div class="modal-row-10">
    <span class="w-32 mr-4">{{ title }}:</span>
    <ripple-button class="btn btn-primary w-12 h-full text-2xl" @click="addItem" v-if="stringArray.length === 0">
      +
    </ripple-button>
    <template v-else>
      <input class="flex-1 modal-input" type="text" v-model="stringArray[0]" />
      <ripple-button class="btn btn-danger w-12 h-full ml-2 text-2xl" @click="deleteItem(0)"> x </ripple-button>
    </template>
  </div>
  <template v-if="stringArray.length > 0">
    <div class="modal-row-10" v-for="i in stringArray.length - 1" :key="i">
      <span class="w-32 mr-4"></span>
      <input class="flex-1 modal-input" type="text" v-model="stringArray[i]" />
      <ripple-button class="btn btn-danger w-12 h-full ml-2 text-2xl" @click="deleteItem(i)"> x </ripple-button>
    </div>
    <div class="modal-row-10">
      <span class="w-32 mr-4"></span>
      <ripple-button class="btn btn-primary w-12 h-full text-2xl" @click="addItem"> + </ripple-button>
    </div>
  </template>
</template>
