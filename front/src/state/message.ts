import { reactive } from "vue";

export interface Message {
  detail: string;
}

export interface MessageState {
  queue: Array<Message>;
  messages: Array<Message>;
  push: (detail: string) => void;
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
});
