export interface Point {
  x: Number;
  y: Number;
}

export interface Selection {
  color: String;
  isCompleted: Boolean;
  points: Array<Point>;
  name?: String;
}

export interface Layer {
  name?: String;
  show: Boolean;
  selections: Array<Selection>;
}

export interface Current {
  layer: Number;
  selection: Number;
}

export interface LayerState {
  current: Current;
  isEdit: Boolean;
  layers: Array<Layer>;
}
