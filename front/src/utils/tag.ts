import { reactive } from "vue";

import { SelectDropdownOption } from "@/elements/Dropdown/SelectDropdown.vue";

import { getTagInterpretation, TagInterpretation } from "@/api/v1/tag/tag";

const tips = reactive({});

export function tagToStr(tag: TagInterpretation) {
  let s = `id:\n    ${tag.id}\n`;
  s += `\nname:\n    ${tag.name}\n`;

  if (tag.representative) {
    s += `\nrepresentative:\n    ${tag.representative.name}\n`;
  }

  if (tag.categories.length > 0) {
    const tagCategories = [];
    for (const c of tag.categories) {
      tagCategories.push(c.name);
    }
    const tagCategoriesStr = tagCategories.join(", ");
    s += `\ncategories:\n    ${tagCategoriesStr}\n`;
  }

  if (tag.synonyms.length > 0) {
    const tagSynonyms = [];
    for (const s of tag.synonyms) {
      tagSynonyms.push(s.name);
    }
    const tagSynonymsStr = tagSynonyms.join(", ");
    s += `\nsynonyms:\n    ${tagSynonymsStr}\n`;
  }

  for (const attr of tag.attributes) {
    s += `\n${attr.name}:\n    ${attr.value}\n`;
  }

  return s;
}

export function onGetTip(opt: SelectDropdownOption) {
  if (tips[opt.value]) {
    return tagToStr(tips[opt.value]);
  }
  return undefined;
}

export function onMouseoverOption(_: any, opt: SelectDropdownOption) {
  if (tips[opt.value] !== undefined) {
    return;
  }
  getTagInterpretation(opt.value).then((response) => {
    const tag = response.data as TagInterpretation;
    tips[opt.value] = tag;
  });
}
