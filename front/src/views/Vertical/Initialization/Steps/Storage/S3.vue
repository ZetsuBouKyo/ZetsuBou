<script setup lang="ts">
import { PropType, reactive, watch } from "vue";

import { StepState } from "@/views/Vertical/Initialization/Step.interface";

import Step from "@/views/Vertical/Initialization/Step.vue";

const props = defineProps({
    step: {
        type: Object as PropType<StepState>,
        required: true,
    },
});

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
</script>

<template>
    <step :state="step">
        <template v-slot:body>
            <div class="views-setting-row-12">
                <span class="views-setting-cell w-64">Access key ID:&emsp;</span>
                <input
                    class="views-setting-cell w-72"
                    type="text"
                    autocomplete="new-password"
                    v-model="step.setting.storage_s3_aws_access_key_id"
                />
            </div>
            <div class="views-setting-row-12">
                <span class="views-setting-cell w-64">Secret access key:&emsp;</span>
                <input
                    class="views-setting-cell w-72"
                    type="password"
                    autocomplete="new-password"
                    v-model="step.setting.storage_s3_aws_secret_access_key"
                />
            </div>
            <div class="views-setting-row-12">
                <span class="views-setting-cell w-64">Confirm secret access key:&emsp;</span>
                <input
                    class="views-setting-cell w-72"
                    type="password"
                    autocomplete="new-password"
                    v-model="state.secretAccessKey"
                />
            </div>
            <div class="views-setting-row-12">
                <span class="views-setting-cell w-64">Volume:&emsp;</span>
                <input
                    class="views-setting-cell w-72"
                    type="text"
                    autocomplete="new-password"
                    placeholder="./dev/volumes/minio"
                    v-model="step.setting.storage_s3_volume"
                />
            </div>
        </template>
    </step>
</template>
