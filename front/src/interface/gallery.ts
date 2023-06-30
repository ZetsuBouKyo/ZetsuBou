import { Source } from "@/interface/source";

export interface Attributes {
  name: string;
  raw_name: string;
  uploader: string;
  category: string;
  rating: string | number;
  src: string;
}

export interface Gallery extends Source {
  group: string;
  mtime: string;
  attributes: Attributes;
}
