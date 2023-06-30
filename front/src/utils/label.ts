import { SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.vue";

import { Source, SourceDataState } from "@/interface/source";

export function watchLabelsLength(
  labelsState?: SelectDropdownState,
  sourceState?: SourceDataState<Source>,
): [any, any] {
  return [
    () => sourceState.data.labels.length,
    () => {
      labelsState.chips = [];
      if (sourceState.data.labels) {
        for (const label of sourceState.data.labels) {
          labelsState.chips.push({ title: label, value: undefined });
        }
      }
    },
  ];
}

export function watchLabelsChipsLength(
  labelsState?: SelectDropdownState,
  sourceState?: SourceDataState<Source>,
): [any, any] {
  return [
    () => labelsState.chips.length,
    () => {
      if (labelsState.chips !== undefined) {
        sourceState.data.labels = [];
        for (const chip of labelsState.chips) {
          sourceState.data.labels.push(chip.title);
        }
      }
    },
  ];
}
