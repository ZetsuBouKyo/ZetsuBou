import { reactive } from "vue";

import { AxiosResponse } from "axios";

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
  sendAirflowMessage: (
    response: AxiosResponse,
    queuedMessage: string,
    successMessage: string,
    failedMessage: string,
  ) => void;
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
  sendAirflowMessage: (
    response: AxiosResponse,
    queuedMessage: string,
    successMessage: string,
    failedMessage: string,
  ) => {
    const data: AirflowDagRunResponse = response.data;

    switch (data.state) {
      case AirflowDagRunStateEnum.Queued:
        const task: AirflowTask = {
          dagID: data.dag_id,
          dagRunID: data.dag_run_id,
          state: data.state,
          successMessage: successMessage,
        };
        messageState.push(queuedMessage);
        messageState.pushAirflowTask(task);
        break;
      case AirflowDagRunStateEnum.Failed:
        messageState.push(failedMessage);
        break;
      default:
        break;
    }
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
