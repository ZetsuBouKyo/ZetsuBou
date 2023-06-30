import { reactive } from "vue";

import SelectDropdown, { SelectDropdownOption, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.vue";

import { TagFieldsPrivateState } from "@/interface/tag";
import { Source, SourceDataState } from "@/interface/source";

import { getTagInterpretation, TagInterpretation } from "@/api/v1/tag/tag";
import { getTagTokenStartWith } from "@/api/v1/tag/token";
import { GetTagTokenStartWithParam } from "@/api/v1/tag/token.d";

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

export function watchTags(
  privateState?: TagFieldsPrivateState,
  tagFieldsState?: SelectDropdownState,
  sourceState?: SourceDataState<Source>,
): [any, any] {
  return [
    () => JSON.stringify(sourceState.data.tags),
    (currentLength: number, _: number) => {
      if (currentLength !== tagFieldsState.chips.length) {
        tagFieldsState.chips = [];
        privateState.tagFields = {};
        for (const field in sourceState.data.tags) {
          tagFieldsState.chips.push({ title: field, value: undefined });
          privateState.tagFields[field] = SelectDropdown.initState() as SelectDropdownState;
          privateState.onGets[field] = (params: GetTagTokenStartWithParam) => {
            params.category = field;
            return getTagTokenStartWith(params);
          };

          for (const tagValue of sourceState.data.tags[field]) {
            privateState.tagFields[field].chips.push({ title: tagValue, value: undefined });
          }
        }
      }
    },
  ];
}

export function watchTagFieldsChipsLength(
  privateState?: TagFieldsPrivateState,
  tagFieldsState?: SelectDropdownState,
  sourceState?: SourceDataState<Source>,
): [any, any] {
  return [
    () => tagFieldsState.chips.length,
    (currentLength: number, _: number) => {
      if (currentLength !== Object.keys(sourceState.data.tags).length) {
        const chipTitles = [];
        for (const chip of tagFieldsState.chips) {
          if (privateState.tagFields[chip.title] === undefined) {
            privateState.tagFields[chip.title] = SelectDropdown.initState() as SelectDropdownState;
            privateState.onGets[chip.title] = (params) => {
              params.category = chip.title;
              return getTagTokenStartWith(params);
            };
          }
          if (sourceState.data.tags[chip.title] === undefined) {
            sourceState.data.tags[chip.title] = [];
          }
          chipTitles.push(chip.title);
        }
        for (const field in privateState.tagFields) {
          if (!chipTitles.includes(field)) {
            delete privateState.tagFields[field];
            delete privateState.onGets[field];
          }
        }
        for (const field in sourceState.data.tags) {
          if (!chipTitles.includes(field)) {
            delete sourceState.data.tags[field];
          }
        }
      }
    },
  ];
}
