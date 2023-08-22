import { SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";

import { Source, SourceDataState } from "@/interface/source";

function updateLabel(labelsState?: SelectDropdownState, sourceState?: SourceDataState<Source>) {
  if (!sourceState?.data) {
    return;
  }
  labelsState.chips = [];
  if (sourceState.data.labels) {
    for (const label of sourceState.data.labels) {
      labelsState.chips.push({ title: label, value: undefined });
    }
  }
}

export function watchLabels(labelsState?: SelectDropdownState, sourceState?: SourceDataState<Source>): [any, any] {
  updateLabel(labelsState, sourceState);
  return [
    () => JSON.stringify(sourceState.data.labels),
    () => {
      updateLabel(labelsState, sourceState);
    },
  ];
}

function updateLabelsChipsLength(labelsState?: SelectDropdownState, sourceState?: SourceDataState<Source>) {
  if (!sourceState?.data) {
    return;
  }
  if (labelsState.chips !== undefined) {
    sourceState.data.labels = [];
    for (const chip of labelsState.chips) {
      sourceState.data.labels.push(chip.title as string);
    }
  }
}

export function watchLabelsChipsLength(
  labelsState?: SelectDropdownState,
  sourceState?: SourceDataState<Source>,
): [any, any] {
  updateLabelsChipsLength(labelsState, sourceState);
  return [
    () => labelsState.chips.length,
    () => {
      updateLabelsChipsLength(labelsState, sourceState);
    },
  ];
}
