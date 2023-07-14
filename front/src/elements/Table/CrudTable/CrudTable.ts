import { reactive } from "vue";

import { Row, CrudTableState } from "./interface";

export function initCrudTableState(row?: Row): CrudTableState<Row> {
  return reactive<CrudTableState<Row>>({
    sheet: undefined,
    pagination: undefined,
    row: row,
    cache: undefined,
    editor: {
      handler: undefined,
      title: undefined,
    },
  });
}
