<script setup>
const modelValue = defineModel();

function toggleSwitch() {
    modelValue.value = !modelValue.value;
}
</script>

<template>
    <div
        class="relative inline-flex items-center cursor-pointer rounded-full h-8"
        :class="{ 'bg-indigo-500': modelValue, 'bg-gray-300': !modelValue }"
        @click="toggleSwitch"
    >
        <span class="inline-block w-14 h-8 rounded-full transition-colors duration-300 ease-in-out"></span>
        <span
            class="absolute left-0 inline-block w-6 h-6 bg-white rounded-full shadow transform transition-transform duration-300 ease-in-out"
            :class="{ 'translate-x-7': modelValue, 'translate-x-1': !modelValue }"
        ></span>
    </div>
</template>
