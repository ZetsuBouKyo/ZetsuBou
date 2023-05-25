import { reactive } from "vue";

import { getSettingFrontGeneral } from "@/api/v1/setting/front/front";

import { SearchAnalyzer } from "@/interface/search";

export interface GeneralAnalyzerFieldSetting {
  [key: string]: Array<string>;
}

export type GeneralAnalyzerKeywordSetting = {
  [key in SearchAnalyzer]: Array<string>;
};

export interface GeneralAnalyzerSetting {
  field: GeneralAnalyzerFieldSetting;
  keyword: GeneralAnalyzerKeywordSetting;
}

export interface GeneralGallerySetting {
  analyzer: GeneralAnalyzerSetting;
}

export interface GeneralVideoSetting {
  analyzer: GeneralAnalyzerSetting;
}

export interface GeneralSetting {
  gallery: GeneralGallerySetting;
  video: GeneralVideoSetting;
}

export interface Setting {
  init: () => void;
  setting: GeneralSetting;
}

export const settingState = reactive<Setting>({
  setting: undefined,
  init: () => {
    getSettingFrontGeneral().then((response) => {
      const data: GeneralSetting = response.data;
      settingState.setting = data;
    });
  },
});
