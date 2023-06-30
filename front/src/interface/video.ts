import { Tags } from "@/interface/tag";

export interface VideoAttributes {
  category: string;
  rating: number;
  height: number;
  width: number;
  uploader: string;
  duration: number;
  fps: number;
  frames: number;
  md5: string;
  src: string;
}

export interface Video {
  id: string;
  name: string;
  other_names: Array<string>;
  path: string;
  attributes: VideoAttributes;
  tags: Tags;
  labels: Array<string>;
  timestamp: string;
}
