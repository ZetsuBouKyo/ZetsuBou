<script setup lang="ts">
import { reactive } from "vue";

import { Setting } from "@/interface/setting";

import CheckHostPortsStep from "./Steps/CheckHostPorts.vue";
import Finished from "./Steps/Finished.vue";
import S3 from "./Steps/Storage/S3.vue";
import ZetsuBouStep from "./Steps/ZetsuBou.vue";

import { initStepState } from "./Step";

const setting = reactive<Setting>({});
const checkHostPorts = initStepState(0, "Check host ports", false);
const zetsubou = initStepState(1, "ZetsuBou Webapp", true);
zetsubou.setting = setting;
const s3 = initStepState(2, "S3 Storage", true);
s3.setting = setting;
const finished = initStepState(3, "Finished", true);
finished.setting = setting;

const steps = [checkHostPorts, zetsubou, s3, finished];
checkHostPorts.steps = steps;
zetsubou.steps = steps;
s3.steps = steps;
finished.steps = steps;
</script>

<template>
  <div class="layout-container">
    <ol class="relative border-l border-gray-200 dark:border-gray-700">
      <check-host-ports-step :step="checkHostPorts" />
      <zetsu-bou-step :step="zetsubou" />
      <s3 :step="s3" />
      <finished :step="finished" />
    </ol>
  </div>
</template>
