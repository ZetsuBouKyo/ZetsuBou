<template>
  <div class="views-setting-section">
    <span class="views-setting-section-title">Video</span>
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
          :mode="SelectDropdownMode.InputChips"
        />
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
          :mode="SelectDropdownMode.InputChips"
        />
      </div>
      <div class="views-setting-row">
        <ripple-button class="flex btn btn-primary ml-auto" @click="save">Save</ripple-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { onGetTip, onMouseoverOption } from "@/utils/tag";

import RippleButton from "@/elements/Button/RippleButton.vue";
import SelectDropdown, {
  SelectDropdownState,
  SelectDropdownMode,
  Origin,
} from "@/elements/Dropdown/SelectDropdown.vue";

import { getSettingFrontVideoInterpretation, putSettingFrontVideo } from "@/api/v1/setting/front/video";
import { getTagTokenStartWith } from "@/api/v1/tag/token";

export default {
  components: { RippleButton, SelectDropdown },
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
      getSettingFrontVideoInterpretation().then((response) => {
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

      putSettingFrontVideo(query).then(() => {
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
