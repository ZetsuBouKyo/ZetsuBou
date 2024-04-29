<script setup lang="ts">
import { PropType } from "vue";

import { StepState } from "@/views/Vertical/Initialization/Step.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import Step from "../Step.vue";

import { checkHostPorts } from "@/api/v1/init/init";

const props = defineProps({
    step: {
        type: Object as PropType<StepState>,
        required: true,
    },
});

const step = props.step;

function check() {
    checkHostPorts().then((response) => {
        if (response.status === 200) {
            const ports = response.data;
            step.ports = ports;

            for (const port in ports) {
                if (!ports[port]) {
                    return;
                }
            }

            step.next = true;
        }
    });
}
</script>

<template>
    <step :state="step">
        <template v-slot:body>
            <div class="flex w-full">
                <span class="w-full">
                    We need ports: 5430 (PostgreSQL), 5431 (PostgreSQL), 5555 (flower), 6379 (Redis), 6380 (Redis), 8080
                    (Airflow), 9000 (MinIO), 9001 (MinIO), and 9200 (Elasticsearch) in host to serve the ZetsuBou
                    webapp.
                </span>
            </div>
            <div class="flex flex-col bg-black text-gray-300 p-4 rounded-lg my-2" v-if="step.ports">
                <div class="flex flex-row items-center" v-for="(isPort, port, i) in step.ports" :key="i">
                    <span class="flex">{{ port }}:&emsp;</span>
                    <span class="flex text-green-500" v-if="isPort">ok</span>
                    <span class="flex text-red-500" v-else>not available</span>
                </div>
            </div>
        </template>
        <template v-slot:buttons>
            <ripple-button class="flex btn btn-primary" @click="check">Check</ripple-button>
        </template>
    </step>
</template>
