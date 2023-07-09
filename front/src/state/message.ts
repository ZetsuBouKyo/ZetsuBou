import { reactive } from "vue";

import { AxiosResponse } from "axios";

import { AirflowDagRunResponse, AirflowDagRunStateEnum, AirflowTask } from "@/interface/airflow";
import { localStorageKey } from "@/interface/localStorage";

import { getUUID } from "@/utils/str";

import { getAirflowDagRun } from "@/api/v1/task/airflow";

export interface Message {
  id: string;
  detail: string;
  link?: string;
  lock?: boolean;
  timeout?: ReturnType<typeof setTimeout>;
  lastUpdated?: string;
}

export interface MessageState {
  queue: Array<Message>;
  history: Array<Message>;
  getHistory: () => Array<Message>;
  clearHistory: () => void;
  push: (detail: string) => void;
  pushWithLink: (detail: string, link: string) => void;
  pushHistory: (message: Message) => void;
  pushError: (error: any) => Promise<AxiosResponse<any>>;
  shiftQueue: (id: string) => void;
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

function _push(message: Message) {
  messageState.queue.push(message);
  messageState.pushHistory(message);
  message.timeout = setTimeout(() => {
    if (!message.lock) {
      messageState.queue = messageState.queue.filter(function (_message: Message) {
        return _message.id !== message.id;
      });
    }
    clearTimeout(message.timeout);
    message.timeout = undefined;
  }, 3000);
  messageState.getHistory();
}

export const messageState = reactive<MessageState>({
  queue: [],
  history: [],
  getHistory: () => {
    const historyString = localStorage.getItem(localStorageKey.Message);
    const history = JSON.parse(historyString) as Array<Message>;
    if (history === null) {
      return [];
    }
    messageState.history = history;
    return history;
  },
  clearHistory: () => {
    localStorage.removeItem(localStorageKey.Message);
    messageState.getHistory();
  },
  push: (detail: string) => {
    const message: Message = { id: getUUID(), detail: detail, lastUpdated: new Date().toLocaleString() };
    _push(message);
  },
  pushWithLink: (detail: string, link: string) => {
    const message: Message = { id: getUUID(), detail: detail, lastUpdated: new Date().toLocaleString(), link: link };
    _push(message);
  },
  pushHistory: (message: Message) => {
    const history = messageState.getHistory();
    history.unshift(message);
    localStorage.setItem(localStorageKey.Message, JSON.stringify(history));
  },
  pushError: (error: any) => {
    const detail = error.response.data.detail;
    if (detail !== undefined) {
      messageState.push(detail);
    } else {
      messageState.push(error);
    }
    return Promise.reject(error);
  },
  shiftQueue: (id: string) => {
    messageState.queue = messageState.queue.filter(function (_message: Message) {
      return _message.id !== id;
    });
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
}, 3000);
