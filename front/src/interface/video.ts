import { Source } from "@/interface/source";

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

export interface Video extends Source {
  name: string;
  other_names: Array<string>;
  attributes: VideoAttributes;
}
