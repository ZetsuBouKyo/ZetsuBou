import { reactive } from "vue";

import { userState } from "@/state/user";
import { getUserCurrentQuestProgress } from "@/api/v1/user/quest/quest";

export interface Progress {
  title: string;
  style: string;
}

export interface ProgressState {
  data: Progress;
  init: Function;
}

export const progressState = reactive<ProgressState>({
  data: {
    title: undefined,
    style: undefined,
  },
  init: () => {
    const user_id = userState.id;
    getUserCurrentQuestProgress(user_id).then((response) => {
      const data = response.data;
      if (data) {
        const numerator = data.numerator;
        const denominator = data.denominator;
        if (numerator === undefined || denominator === undefined || denominator === 0) {
          return;
        }

        const percentage = ((numerator / denominator) * 100).toFixed(2);
        progressState.data.style = `width: ${percentage}%`;
        progressState.data.title = `${percentage}% ( ${numerator} / ${denominator} )`;
      }
    });
  },
});
