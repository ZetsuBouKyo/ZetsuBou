import { BaseState } from "@/interface/state";
import { Setting } from "@/interface/setting";

export interface SettingSystemState extends BaseState<Setting> {
  save: () => void;
}
