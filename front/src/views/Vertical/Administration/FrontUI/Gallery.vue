<template>
  <div class="flex flex-col bg-gray-900 rounded-lg">
    <span class="text-xl text-white font-medium bg-black px-4 py-3 rounded-t-lg">Gallery</span>
    <div class="flex flex-col my-1">
      <div class="modal-row">
        <span class="w-32 mr-4">Categories:</span>
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
          :mode="SelectDropdownMode.InputChips"
        />
      </div>
      <div class="modal-row">
        <span class="w-32 mr-4">Tag fields:</span>
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
          :mode="SelectDropdownMode.InputChips"
        />
      </div>
      <div class="modal-row">
        <button class="flex ml-auto btn btn-primary" @click="save">Save</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { onGetTip, onMouseoverOption } from "@/utils/tag";

import SelectDropdown, {
  SelectDropdownState,
  SelectDropdownMode,
  Origin,
} from "@/elements/Dropdown/SelectDropdown.vue";

import { getSettingFrontGalleryInterpretation, putSettingFrontGallery } from "@/api/v1/setting/front/gallery";
import { getTagTokenStartWith } from "@/api/v1/tag/token";

export default {
  components: { SelectDropdown },
  setup() {
    function tokenToOption(token: { id: number; name: string }) {
      return { title: token.name, value: token.id };
    }

    const categories = SelectDropdown.initState() as SelectDropdownState;
    const onGetCategories = getTagTokenStartWith;
    const onGetCategoriesToOptions = tokenToOption;

    const tagFields = SelectDropdown.initState() as SelectDropdownState;
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

    return {
      SelectDropdownMode,
      Origin,
      categories,
      onGetCategories,
      onGetCategoriesToOptions,
      tagFields,
      onGetTagFields,
      onGetTagFieldsToOptions,
      onGetTip,
      onMouseoverOption,
      save,
    };
  },
};
</script>
