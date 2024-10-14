<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

onMounted(async () => {
    await router.isReady();
});
</script>
<template>
    <main>
        <router-view class="text-gray-400" />
    </main>
</template>
