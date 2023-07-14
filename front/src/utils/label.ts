import { SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";

import { Source, SourceDataState } from "@/interface/source";

export function watchLabels(labelsState?: SelectDropdownState, sourceState?: SourceDataState<Source>): [any, any] {
  return [
    () => JSON.stringify(sourceState.data.labels),
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
          sourceState.data.labels.push(chip.title as string);
        }
      }
    },
  ];
}
