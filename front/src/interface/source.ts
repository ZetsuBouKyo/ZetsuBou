import { Tags } from "@/interface/tag";

export interface SourceAttributes {
    category?: string;
    rating?: number;
    uploader?: string;
}
export interface Source {
    id?: string;
    path?: string;
    name?: string;
    raw_name?: string;
    other_names?: Array<string>;
    src?: Array<string>;
    last_updated?: string;
    publication_date?: string;
    upload_date?: string;
    labels?: Array<string>;
    tags?: Tags;
    attributes?: SourceAttributes;
}
