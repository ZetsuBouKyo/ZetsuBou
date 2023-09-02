import { Source } from "@/interface/source";
import { SourceState } from "@/interface/state";

export function cleanData(state: SourceState<Source>) {
  if (state.data.id) {
    state.data.id = state.data.id.trim();
  }
  if (state.data.name) {
    state.data.name = state.data.name.trim();
  }
  if (state.data.raw_name) {
    state.data.raw_name = state.data.raw_name.trim();
  }

  // clean attributes
  for (const attr in state.data.attributes) {
    if (typeof state.data.attributes[attr] === "string") {
      if (state.data.attributes[attr].length === 0) {
        state.data.attributes[attr] = null;
      } else {
        state.data.attributes[attr] = state.data.attributes[attr].trim();
      }
    }
  }

  // clean tags
  const emptyTagFields = [];
  for (const field in state.data.tags) {
    if (state.data.tags[field] === undefined || state.data.tags[field].length === 0) {
      emptyTagFields.push(field);
    }
  }
  for (const field of emptyTagFields) {
    delete state.data.tags[field];
  }
}
