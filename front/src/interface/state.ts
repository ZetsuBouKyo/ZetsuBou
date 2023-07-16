export interface BaseState<DataT> {
  data: DataT;
  init?: () => void;
}
