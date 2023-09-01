import { Source, SourceAttributes } from "@/interface/source";

export interface VideoAttributes extends SourceAttributes {
  width: number;
  height: number;
  duration: number;
  fps: number;
  frames: number;
  md5: string;
}

export interface Video extends Source {
  attributes: VideoAttributes;
}
