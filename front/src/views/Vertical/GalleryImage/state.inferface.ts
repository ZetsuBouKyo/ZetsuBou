export interface Point {
  x: number;
  y: number;
}

export interface Selection {
  color: string;
  isCompleted: boolean;
  points: Array<Point>;
  name?: string;
}

export interface Layer {
  name?: string;
  show: boolean;
  selections: Array<Selection>;
}

export interface Current {
  layer: number;
  selection: number;
}

export interface Layers {
  current: Current;
  isEdit: boolean;
  layers: Array<Layer>;
}

export interface Container {
  gallery: string | string[];
  imgName: string | string[];
  imgUrl?: string;
  imgWidth?: number;
  imgHeight?: number;
  defaultGridStep: number;
  defaultOriginX: number;
  defaultOriginY: number;
  defaultRotation: number;
  defaultScale: number;
  gridStep: number;
  originX: number;
  originY: number;
  rotation: number;
  scale: number;
  scaleFactor: number;
  dragStart: Point | null;
}

export interface Sidebar {
  isRuler: boolean;
  isSidebar: boolean;
  activateSidebar: () => void;
  closeSidebar: () => void;
  toggleSidebar: () => void;
}

export interface Bookmark {
  id?: number;
  user_id?: number;
  gallery_id?: string;
  page?: number;
  isBookmark: boolean;
}

export interface Panel {
  imgs: [];
  galleryID: string;
  imgName: string;
  timeInterval: number;
  current: number;
  isPlay: boolean;
  play: ReturnType<typeof setInterval>;
}

export interface RotationModal {
  open: () => void;
  close: () => void;
}

export interface Modal {
  rotation: RotationModal | undefined;
}

export interface GalleryImageState {
  container: Container;
  bookmark?: Bookmark;
  sidebar: Sidebar;
  panel: Panel;
  layers: Layers;
  modal: Modal;
}
