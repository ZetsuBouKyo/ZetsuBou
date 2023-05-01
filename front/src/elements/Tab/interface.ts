export interface Tab {
  title: string;
  active: boolean;
  link: string;
}

export interface Tabs extends Array<Tab> {}
