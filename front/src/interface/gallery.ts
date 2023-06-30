import { Tags } from "@/interface/tag";

export interface Attributes {
  name: string;
  raw_name: string;
  uploader: string;
  category: string;
  rating: string | number;
  src: string;
}

export interface Gallery {
  id: string;
  path: string;
  group: string;
  timestamp: string;
  mtime: string;
  attributes: Attributes;
  tags: Tags;
  labels: Array<string>;
}
