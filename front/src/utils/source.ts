import { Source } from "@/interface/source";
import { SourceState } from "@/interface/state";

function cleanStringArray(arr: Array<string>): Array<string> {
    const newArray = [];
    for (const a of arr) {
        if (a) {
            newArray.push(a);
        }
    }
    return newArray;
}

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

    if (state.data.other_names.length > 0) {
        state.data.other_names = cleanStringArray(state.data.other_names);
    }

    if (state.data.src.length > 0) {
        state.data.src = cleanStringArray(state.data.src);
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
