<template>
  <div>
    <div class="overflow-hidden h-1 text-xxs flex rounded bg-gray-300" v-if="progressState.data.style">
      <div
        :style="progressState.data.style"
        class="shadow-none flex flex-col rounded-sm text-center whitespace-nowrap text-white justify-center bg-indigo-500"
      ></div>
    </div>
  </div>
</template>

<script>
import { progressState } from "./progress";
export default {
  setup() {
    return { progressState };
  },
};
</script>
