import { Source, SourceAttributes } from "@/interface/source";

export interface Attributes extends SourceAttributes {
    pages: number;
}

export interface Gallery extends Source {
    attributes: Attributes;
}
