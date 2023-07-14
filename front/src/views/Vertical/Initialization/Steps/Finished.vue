<script setup lang="ts">
import { PropType } from "vue";

import { StepState } from "@/views/Vertical/Initialization/Step.interface";

import Step from "../Step.vue";

import { postSettingSystem, postSettingSystemAirflow } from "@/api/v1/setting/system";

const props = defineProps({
  step: {
    type: Object as PropType<StepState>,
    required: true,
  },
});

const step = props.step;

function onFinish(state: StepState) {
  const setting = state.setting;
  if (setting === undefined || !setting) {
    return;
  }
  postSettingSystem(setting).then((response) => {});
  postSettingSystemAirflow(setting).then((response) => {});
}
</script>

<template>
  <step :state="step" :on-finish="onFinish">
    <template v-slot:body>
      <div class="flex w-full">
        <span class="w-full"> We will generate `./etc/setting.env` and `./etc/setting.airflow.env`.</span>
      </div>
    </template>
  </step>
</template>
