<template>
  <step :state="step">
    <template v-slot:body>
      <div class="views-setting-row">
        <span class="views-setting-cell w-64">Access key ID:&emsp;</span>
        <input
          class="views-setting-cell w-72"
          type="text"
          autocomplete="new-password"
          v-model="step.setting.storage_s3_aws_access_key_id" />
      </div>
      <div class="views-setting-row">
        <span class="views-setting-cell w-64">Secret access key:&emsp;</span>
        <input
          class="views-setting-cell w-72"
          type="password"
          autocomplete="new-password"
          v-model="step.setting.storage_s3_aws_secret_access_key" />
      </div>
      <div class="views-setting-row">
        <span class="views-setting-cell w-64">Confirm secret access key:&emsp;</span>
        <input
          class="views-setting-cell w-72"
          type="password"
          autocomplete="new-password"
          v-model="state.secretAccessKey" />
      </div>
      <div class="views-setting-row">
        <span class="views-setting-cell w-64">Volume:&emsp;</span>
        <input
          class="views-setting-cell w-72"
          type="text"
          autocomplete="new-password"
          placeholder="./dev/volumes/minio"
          v-model="step.setting.storage_s3_volume" />
      </div>
    </template>
  </step>
</template>

<script lang="ts">
import { PropType, reactive, watch } from "vue";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Step, { StepState } from "@/views/Vertical/Initialization/Step.vue";

export default {
  components: { RippleButton, Step },
  props: {
    step: {
      type: Object as PropType<StepState>,
      default: undefined,
    },
  },
  setup(props) {
    const step = props.step;

    const state = reactive({
      secretAccessKey: undefined,
    });

    watch(
      () => {
        return [
          step.setting.storage_s3_aws_access_key_id,
          step.setting.storage_s3_aws_secret_access_key,
          state.secretAccessKey,
          step.setting.storage_s3_volume,
        ];
      },
      () => {
        if (
          step.setting.storage_s3_aws_access_key_id &&
          step.setting.storage_s3_aws_secret_access_key &&
          state.secretAccessKey &&
          step.setting.storage_s3_aws_secret_access_key === state.secretAccessKey &&
          step.setting.storage_s3_volume
        ) {
          step.next = true;
        } else {
          step.next = false;
        }
      },
    );

    return { state, step };
  },
};
</script>
