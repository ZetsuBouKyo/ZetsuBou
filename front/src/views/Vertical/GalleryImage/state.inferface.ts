export interface Point {
    x: number;
    y: number;
}

export interface Container {
    gallery: string | string[];
    imgName: string | string[];
    imgUrl?: string;
    imgWidth?: number;
    imgHeight?: number;
    defaultGridAlpha: number;
    defaultGridLineWidth: number;
    defaultGridStep: number;
    defaultOriginX: number;
    defaultOriginY: number;
    defaultRotation: number;
    defaultScale: number;
    gridAlpha: number;
    gridLineWidth: number;
    gridStep: number;
    originX: number;
    originY: number;
    rotation: number;
    scale: number;
    scaleFactor: number;
    dragStart: Point | null;
}

export enum GalleryImageSideBarEnum {
    Cursor = "cursor",
    Grid = "grid",
    Polygon = "polygon",
    Rotation = "rotation",
}
export interface SidebarGrid {
    alpha: number | undefined;
    lineWidth: number | undefined;
    step: number | undefined;
}

export interface Polygon {
    id: number;
    name?: string;
    points: Array<Point>;
    lineWidth?: number;
    color?: string;
    isVisible: boolean;
    isCompleted: boolean;
}

export interface Polygons {
    [key: number]: Polygon;
}

export interface SidebarPolygon {
    startID: number;
    currentID: number | undefined;
    polygons: Polygons;
}

export interface SidebarRotation {
    degree: number | undefined;
}

export interface Sidebar {
    isGrid: boolean;
    isSidebar: boolean;
    isSubSidebar: boolean;
    category: GalleryImageSideBarEnum;
    grid: SidebarGrid;
    polygon: SidebarPolygon;
    rotation: SidebarRotation;
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

export interface GalleryImageState {
    container: Container;
    bookmark?: Bookmark;
    sidebar: Sidebar;
    panel: Panel;
}
