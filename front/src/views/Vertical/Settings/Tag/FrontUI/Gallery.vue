<script setup lang="ts">
import { Origin } from "@/elements/Dropdown/Dropdown.interface";
import { SelectDropdownMode, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown from "@/elements/Dropdown/SelectDropdown.vue";

import { getSettingFrontGalleryInterpretation, putSettingFrontGallery } from "@/api/v1/setting/front/gallery";
import { getTagTokenStartWith } from "@/api/v1/tag/token";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";

import { onGetTip, onMouseoverOption } from "@/utils/tag";

function tokenToOption(token: { id: number; name: string }) {
  return { title: token.name, value: token.id };
}

const categories = initSelectDropdownState() as SelectDropdownState;
const onGetCategories = getTagTokenStartWith;
const onGetCategoriesToOptions = tokenToOption;

const tagFields = initSelectDropdownState() as SelectDropdownState;
const onGetTagFields = getTagTokenStartWith;
const onGetTagFieldsToOptions = tokenToOption;

function load() {
  getSettingFrontGalleryInterpretation().then((response) => {
    const data = response.data as any;
    for (let i = 0; i < data.categories.length; i++) {
      const token = data.categories[i];
      const chip = tokenToOption(token);
      categories.chips.push(chip);
    }
    for (let i = 0; i < data.tag_fields.length; i++) {
      const token = data.tag_fields[i];
      const chip = tokenToOption(token);
      tagFields.chips.push(chip);
    }
  });
}
load();

function save() {
  const query = {
    category_ids: [],
    tag_field_ids: [],
  };

  for (let i = 0; i < categories.chips.length; i++) {
    const chip = categories.chips[i];
    query.category_ids.push(chip.value);
  }

  for (let i = 0; i < tagFields.chips.length; i++) {
    const chip = tagFields.chips[i];
    query.tag_field_ids.push(chip.value);
  }

  putSettingFrontGallery(query).then(() => {
    window.location.reload();
  });
}
</script>

<template>
  <div class="views-setting-section">
    <span class="views-setting-section-title">Gallery</span>
    <div class="views-setting-rows">
      <div class="views-setting-row">
        <div class="views-setting-cell w-32">Categories:</div>
        <select-dropdown
          class="flex-1"
          :options-width-class="'w-96'"
          :origin="Origin.BottomLeft"
          :state="categories"
          :enable-input-chips-enter-event="false"
          :on-get="onGetCategories"
          :on-get-to-options="onGetCategoriesToOptions"
          :on-get-tip="onGetTip"
          :on-mouseover-option="onMouseoverOption"
          :mode="SelectDropdownMode.InputChips" />
      </div>
      <div class="views-setting-row">
        <div class="views-setting-cell w-32">Tag fields:</div>
        <select-dropdown
          class="flex-1"
          :options-width-class="'w-96'"
          :origin="Origin.BottomLeft"
          :state="tagFields"
          :enable-input-chips-enter-event="false"
          :on-get="onGetTagFields"
          :on-get-to-options="onGetTagFieldsToOptions"
          :on-get-tip="onGetTip"
          :on-mouseover-option="onMouseoverOption"
          :mode="SelectDropdownMode.InputChips" />
      </div>
      <div class="views-setting-row">
        <ripple-button class="flex btn btn-primary ml-auto" @click="save">Save</ripple-button>
      </div>
    </div>
  </div>
</template>
