import { SelectDropdownState } from "@/elements/Dropdown/SelectDropdown.interface";
import { SearchCategory } from "@/interface/search";

export enum AdvancedSearchFieldType {
    String,
    Range,
    Duration,
}

export enum AdvancedSearchFieldKeyEnum {
    ElasticsearchField,
    BuiltIn,
}

export interface AdvancedSearchField {
    name: string;
    type: AdvancedSearchFieldType;
    value: string;
    key?: string;
    keyType?: AdvancedSearchFieldKeyEnum;
    fuzziness?: SelectDropdownState;
    analyzer?: SelectDropdownState;
    boolean?: SelectDropdownState;
    gte?: number | string;
    lte?: number | string;
}

export interface AdvancedSearchState {
    category: SearchCategory;
    fields: Array<AdvancedSearchField>;
}
