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

export interface Ruler {
    show: boolean;
    isEdit: boolean;
    interval: number;
    color: string;
}

export interface Layers {
    current: Current;
    isEdit: boolean;
    layers: Array<Layer>;
}

export interface Container {
    draggable: boolean;
    viewBox: string;
    imgWidth: number;
    imgHeight: number;
    imgSlope: number;
    xTopLeft: number;
    yTopLeft: number;
    xBottomRight: number;
    yBottomRight: number;
}

export interface Sidebar {
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

export interface SVG {
    container: Container;
    bookmark?: Bookmark;
    sidebar: Sidebar;
    panel: Panel;
    layers: Layers;
    ruler: Ruler;
}
