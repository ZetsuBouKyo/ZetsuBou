import { reactive } from "vue";

import { TagFieldsPrivateState } from "@/interface/tag";
import { Source } from "@/interface/source";
import { DataState } from "@/interface/state";
import { GetTagTokenStartWithParam } from "@/api/v1/tag/token.interface";
import { SelectDropdownOption, SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";

import { getTagInterpretation, TagInterpretation } from "@/api/v1/tag/tag";
import { getTagTokenStartWith } from "@/api/v1/tag/token";

import { initSelectDropdownState } from "@/elements/Dropdown/SelectDropdown";

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

function updateTags(
  privateState?: TagFieldsPrivateState,
  tagFieldsState?: SelectDropdownState,
  sourceState?: DataState<Source>,
) {
  if (sourceState?.data?.tags === undefined) {
    return;
  }
  tagFieldsState.chips = [];
  privateState.tagFields = {};
  for (const field in sourceState.data.tags) {
    tagFieldsState.chips.push({ title: field, value: undefined });
    privateState.tagFields[field] = initSelectDropdownState() as SelectDropdownState;
    privateState.onGets[field] = (params: GetTagTokenStartWithParam) => {
      params.category = field;
      return getTagTokenStartWith(params);
    };

    for (const tagValue of sourceState.data.tags[field]) {
      privateState.tagFields[field].chips.push({ title: tagValue, value: undefined });
    }
  }
}

// Update the UI with the sourceState, which is the gallery data.
export function watchTags(
  privateState?: TagFieldsPrivateState,
  tagFieldsState?: SelectDropdownState,
  sourceState?: DataState<Source>,
): [any, any] {
  updateTags(privateState, tagFieldsState, sourceState);
  return [
    () => JSON.stringify(sourceState.data.tags),
    (currentLength: number, _: number) => {
      updateTags(privateState, tagFieldsState, sourceState);
    },
  ];
}

function updateTagFieldsChipsLength(
  privateState?: TagFieldsPrivateState,
  tagFieldsState?: SelectDropdownState,
  sourceState?: DataState<Source>,
) {
  if (sourceState?.data?.tags === undefined) {
    return;
  }
  const chipTitles = [];
  for (const chip of tagFieldsState.chips) {
    if (privateState.tagFields[chip.title] === undefined) {
      privateState.tagFields[chip.title] = initSelectDropdownState() as SelectDropdownState;
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

export function watchTagFieldsChipsLength(
  privateState?: TagFieldsPrivateState,
  tagFieldsState?: SelectDropdownState,
  sourceState?: DataState<Source>,
): [any, any] {
  updateTagFieldsChipsLength(privateState, tagFieldsState, sourceState);
  return [
    () => tagFieldsState.chips.length,
    (currentLength: number, _: number) => {
      if (currentLength !== Object.keys(sourceState.data.tags).length) {
        updateTagFieldsChipsLength(privateState, tagFieldsState, sourceState);
      }
    },
  ];
}

function getTags(privateState?: TagFieldsPrivateState) {
  const tags = {};
  for (const field in privateState.tagFields) {
    const state = privateState.tagFields[field];
    tags[field] = [];
    for (const chip of state.chips) {
      tags[field].push(chip.title);
    }
  }
  return tags;
}

export function watchTagFieldValues(privateState?: TagFieldsPrivateState, sourceState?: DataState<Source>): [any, any] {
  return [
    () => JSON.stringify(getTags(privateState)),
    (currentTags: string, _: string) => {
      const tags = JSON.parse(currentTags);
      if (sourceState?.data?.tags === undefined) {
        return;
      }
      sourceState.data.tags = tags;
    },
  ];
}
