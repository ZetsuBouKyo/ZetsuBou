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
  imgScale?: number;
  scale: number;
  rotation: number;
  originX: number;
  originY: number;
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

export interface Modal {
  rotation: any;
}

export interface GalleryImageState {
  container: Container;
  bookmark?: Bookmark;
  sidebar: Sidebar;
  panel: Panel;
  layers: Layers;
  modal: Modal;
}
