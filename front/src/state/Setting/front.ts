import { reactive } from "vue";

import { getSettingFrontGeneral } from "@/api/v1/setting/front/front";

import { BaseState } from "@/interface/state";
import { SearchAnalyzer } from "@/interface/search";
import { AppModeEnum } from "@/interface/setting";

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

export interface GeneralGallerySettingGoto {
  sync_pages: boolean;
}
export interface GeneralGallerySetting {
  analyzer: GeneralAnalyzerSetting;
  goto: GeneralGallerySettingGoto;
}

export interface GeneralVideoSetting {
  analyzer: GeneralAnalyzerSetting;
}

export interface GeneralSetting {
  app_mode: AppModeEnum;
  gallery: GeneralGallerySetting;
  video: GeneralVideoSetting;
}

export const settingState = reactive<BaseState<GeneralSetting>>({
  data: undefined,
  init: async () => {
    return getSettingFrontGeneral().then((response) => {
      const data: GeneralSetting = response.data;
      settingState.data = data;
    });
  },
});
