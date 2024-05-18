<script setup>
import { computed } from "vue";

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
});

const isOn = computed(() => props.modelValue);

function toggleSwitch() {
  emit("update:modelValue", !isOn.value);
}
</script>

<template>
  <div
    class="relative inline-flex items-center cursor-pointer rounded-full h-8"
    :class="{ 'bg-indigo-500': isOn, 'bg-gray-300': !isOn }"
    @click="toggleSwitch">
    <span class="inline-block w-14 h-8 rounded-full transition-colors duration-300 ease-in-out"></span>
    <span
      class="absolute left-0 inline-block w-6 h-6 bg-white rounded-full shadow transform transition-transform duration-300 ease-in-out"
      :class="{ 'translate-x-7': isOn, 'translate-x-1': !isOn }"></span>
  </div>
</template>
