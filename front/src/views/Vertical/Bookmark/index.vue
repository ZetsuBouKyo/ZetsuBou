<script setup lang="ts">
import Setting from "@/layouts/Setting/index.vue";
import SettingAction from "@/layouts/Setting/SettingAction.vue";
</script>

<template>
    <setting>
        <div class="views-setting-actions">
            <setting-action :title="'Gallery'" :path="'/bookmark/gallery'">
                <icon-grommet-icons-gallery class="views-setting-action-icon" style="font-size: 1.4rem" />
            </setting-action>
            <setting-action :title="'Image'" :path="'/bookmark/video'">
                <icon-ph-video class="views-setting-action-icon" style="font-size: 1.4rem" />
            </setting-action>
        </div>
    </setting>
</template>
