<template>
  <step :state="step" :on-finish="onFinish">
    <template v-slot:body>
      <div class="flex w-full">
        <span class="w-full"> We will generate `./etc/setting.env` and `./etc/setting.airflow.env`.</span>
      </div>
    </template>
  </step>
</template>

<script lang="ts">
import { PropType } from "vue";

import Step, { StepState } from "../Step.vue";

import { postSettingSystem, postSettingSystemAirflow } from "@/api/v1/setting/system";

export default {
  components: { Step },
  props: {
    step: {
      type: Object as PropType<StepState>,
      default: undefined,
    },
  },
  setup(props) {
    const step = props.step;

    function onFinish(state: StepState) {
      const setting = state.setting;
      if (setting === undefined || !setting) {
        return;
      }
      postSettingSystem(setting).then((response) => {});
      postSettingSystemAirflow(setting).then((response) => {});
    }

    return { step, onFinish };
  },
};
</script>
