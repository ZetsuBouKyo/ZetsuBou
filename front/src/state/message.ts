import { reactive } from "vue";

import { AirflowDagRunResponse, AirflowDagRunStateEnum, AirflowTask } from "@/interface/airflow";
import { localStorageKey } from "@/interface/localStorage";

import { getAirflowDagRun } from "@/api/v1/task/airflow";

export interface Message {
  detail: string;
}

export interface MessageState {
  queue: Array<Message>;
  messages: Array<Message>;
  push: (detail: string) => void;
  getAirflowTasks: () => Array<AirflowTask>;
  pushAirflowTask: (task: AirflowTask) => void;
  pushAirflowTasks: (tasks: Array<AirflowTask>) => void;
}

export const messageState = reactive<MessageState>({
  queue: [],
  messages: [],
  push: (detail: string) => {
    const message: Message = { detail: detail };
    messageState.queue.push(message);
    setTimeout(() => {
      messageState.queue.shift();
    }, 3000);
  },
  getAirflowTasks: () => {
    const tasks = localStorage.getItem(localStorageKey.AirflowTasks);
    if (tasks === null) {
      return [];
    }

    const _tasks: Array<AirflowTask> = JSON.parse(tasks);
    return _tasks;
  },
  pushAirflowTask: (task: AirflowTask) => {
    const tasks = messageState.getAirflowTasks();
    tasks.push(task);
    localStorage.setItem(localStorageKey.AirflowTasks, JSON.stringify(tasks));
  },
  pushAirflowTasks: (tasks: Array<AirflowTask>) => {
    localStorage.setItem(localStorageKey.AirflowTasks, JSON.stringify(tasks));
  },
});

setInterval(() => {
  const tasks = messageState.getAirflowTasks();
  const task: AirflowTask = tasks.shift();
  if (task === undefined) {
    return;
  }
  getAirflowDagRun(task.dagID, task.dagRunID).then((response) => {
    const resp: AirflowDagRunResponse = response.data;
    switch (resp.state) {
      case AirflowDagRunStateEnum.Success:
        if (task.successMessage !== undefined) {
          messageState.push(task.successMessage);
        } else {
          messageState.push(`${resp.dag_id} success`);
        }
        break;
      case AirflowDagRunStateEnum.Failed:
        if (task.failedMessage !== undefined) {
          messageState.push(task.failedMessage);
        } else {
          messageState.push(`${resp.dag_id} failed`);
        }
        break;
      default:
        tasks.push(task);
    }
    messageState.pushAirflowTasks(tasks);
  });
}, 1000);
