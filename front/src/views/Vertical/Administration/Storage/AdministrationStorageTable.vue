<template>
  <crud-table
    class="lg:w-2/3 mt-4"
    :state="table"
    :editor-title="'Directory'"
    :headers="headers"
    :colspan="'7'"
    :on-crud-create="onCrudCreate"
    :on-crud-get="onCrudGet"
    :on-crud-get-total="onCrudGetTotal"
    :on-crud-update="onCrudUpdate"
    :on-crud-delete="onCrudDelete"
    :on-open-editor="onOpenEditor"
    :on-close-editor="onCloseEditor"
  >
    <div class="modal-row">
      <span class="w-32 mr-4">Name:</span>
      <input class="flex-1 modal-input" type="text" :placeholder="table.row.name" v-model="table.row.name" />
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Endpoint:</span>
      <input
        class="flex-1 modal-input"
        type="text"
        :placeholder="table.row.endpoint"
        v-model="table.row.endpoint"
        autocomplete="new-password"
      />
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Access key:</span>
      <input
        class="flex-1 modal-input"
        type="password"
        :placeholder="table.row.access_key"
        v-model="table.row.access_key"
        autocomplete="new-password"
      />
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Secret key:</span>
      <input
        class="flex-1 modal-input"
        type="password"
        :placeholder="table.row.secret_key"
        v-model="table.row.secret_key"
        autocomplete="new-password"
      />
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Category:</span>
      <select-dropdown
        class="h-10 w-64"
        :options-width-class="'w-64'"
        :state="categoriesDropdown"
        :on-select="onSelectCategory"
      ></select-dropdown>
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Bucket Name:</span>
      <select-dropdown
        class="h-10 w-64"
        :options-width-class="'w-64'"
        :state="bucketsDropdown"
        :on-select="onSelectBucket"
      ></select-dropdown>
      <span class="ml-4 text-blue-500" v-if="bucketsDropdown.options.length > 0">Connected</span>
      <span class="ml-4 text-red-500" v-else>Failed</span>
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Prefix:</span>
      <input
        class="flex-1 modal-input"
        type="text"
        list="admin-minio-storage-prefix"
        :placeholder="table.row.prefix"
        v-model="table.row.prefix"
        :disabled="!bucketsDropdown.title"
      />
      <datalist id="admin-minio-storage-prefix">
        <option v-for="(p, i) in prefix.options" :value="p" :key="i" />
      </datalist>
    </div>
    <div class="modal-row">
      <span class="w-32 mr-4">Depth:</span>
      <input
        class="flex-1 modal-input"
        type="number"
        list="admin-minio-storage-depth"
        :placeholder="table.row.depth"
        v-model="table.row.depth"
      />
      <datalist id="admin-minio-storage-depth">
        <option v-for="(p, i) in [1, 2, 3, 4, 5, 6, 7]" :value="p" :key="i" />
      </datalist>
    </div>
  </crud-table>
</template>

<script lang="ts">
import { reactive, watch } from "vue";

import { getMinioList } from "@/api/v1/minio/operation";
import {
  getMinioStorageCategories,
  getMinioTotalStorages,
  getMinioStorages,
  postMinioStorage,
  putMinioStorage,
  deleteMinioStorage,
} from "@/api/v1/minio/storage";
import SelectDropdown, { SelectDropdownState, reset } from "@/elements/Dropdown/SelectDropdown.vue";

import CrudTable, { CrudTableState, Header } from "@/elements/Table/CrudTable/index.vue";

export interface Row {
  id?: number;
  category: number;
  name: string;
  endpoint: string;
  bucket_name: string;
  prefix: string;
  depth: number;
  access_key: string;
  secret_key: string;
}

export default {
  components: { CrudTable, SelectDropdown },
  setup() {
    const table = CrudTable.initState() as CrudTableState<Row>;

    const prefix = reactive({
      options: [],
    });

    function getPrefixAutoComplete(bucketName: string, prefixName: string) {
      prefix.options = [];

      if (!bucketName) {
        return;
      }
      if (!table.row.endpoint || !table.row.access_key || !table.row.secret_key) {
        return;
      }

      const params = <
        { bucket_name: string; prefix: string; endpoint: string; access_key: string; secret_key: string }
      >{};
      params.bucket_name = bucketName;
      if (prefixName) {
        params.prefix = prefixName;
      }
      params.endpoint = table.row.endpoint;
      params.access_key = table.row.access_key;
      params.secret_key = table.row.secret_key;
      getMinioList(params)
        .then((response) => {
          const data = response.data;
          if (data) {
            for (let i = 0; i < data.length; i++) {
              const objectName = data[i].object_name;
              if (objectName.slice(-1) === "/") {
                prefix.options.push(objectName);
              }
            }
          }
        })
        .catch(() => {
          minioConnectError();
        });
    }
    watch(
      () => table.row,
      () => {
        const bucketName = bucketsDropdown.selectedValue as string;
        const prefixName = table.row.prefix as string;
        if (bucketName === undefined || prefixName === undefined) {
          return;
        }
        if (prefixName.slice(-1) === "/") {
          getPrefixAutoComplete(bucketName, prefixName);
        }
      },
    );

    const bucketsDropdown = SelectDropdown.initState() as SelectDropdownState;
    function minioConnectError() {
      bucketsDropdown.options = [];
      prefix.options = [];
      table.row.prefix = undefined;
      table.row.bucket_name = undefined;
    }
    function onSelectBucket() {
      table.row.prefix = "";
      const bucketName = bucketsDropdown.selectedValue as string;
      table.row.bucket_name = bucketName;
      getPrefixAutoComplete(bucketName, undefined);
    }
    watch(
      () => {
        if (table.row) {
          return table.row.bucket_name;
        }
        return false;
      },
      () => {
        const bucketName = table.row.bucket_name;
        bucketsDropdown.selectedValue = bucketName;
        bucketsDropdown.title = bucketName;
      },
    );
    watch(
      () => {
        if (table.row === undefined) {
          return false;
        }
        if (
          table.row.endpoint !== undefined &&
          table.row.access_key !== undefined &&
          table.row.secret_key !== undefined &&
          table.row.endpoint.length > 0 &&
          table.row.access_key.length > 0 &&
          table.row.secret_key.length > 0
        ) {
          return [table.row.endpoint, table.row.access_key, table.row.secret_key];
        }
        return false;
      },
      (status, _) => {
        if (!status) {
          return;
        }
        const params = {
          endpoint: table.row.endpoint,
          access_key: table.row.access_key,
          secret_key: table.row.secret_key,
        };
        getMinioList(params)
          .then((response) => {
            if (response.status !== 200) {
              minioConnectError();
              return;
            }
            const data = response.data;
            if (data) {
              for (let i = 0; i < data.length; i++) {
                bucketsDropdown.options.push({ title: data[i].bucket_name, value: data[i].bucket_name });
              }
            }
          })
          .catch(() => {
            minioConnectError();
          });
      },
    );

    const categoriesDropdown = SelectDropdown.initState() as SelectDropdownState;
    function onSelectCategory() {
      table.row.prefix = "";
      const category = categoriesDropdown.selectedValue as number;
      table.row.category = category;
    }
    watch(
      () => {
        if (table.row) {
          return table.row.category;
        }
        return false;
      },
      () => {
        const categoryID = table.row.category;
        categoriesDropdown.selectedValue = categoryID;
        categoriesDropdown.title = getCategoryName(categoryID);
      },
    );

    const categories = reactive({});
    function getCategoryName(id: number) {
      return categories[id];
    }
    getMinioStorageCategories().then((response) => {
      const data = response.data;
      if (data) {
        for (let key in data) {
          categories[data[key]] = key;
        }
      }
    });

    function load() {
      getMinioStorageCategories().then((response) => {
        const data = response.data;
        if (data) {
          for (let key in data) {
            categoriesDropdown.options.push({ title: key, value: data[key] });
          }
        }
      });
    }

    const headers: Array<Header> = [
      { title: "Id", key: "id" },
      { title: "Name", key: "name" },
      { title: "Category", key: "category", handler: getCategoryName },
      { title: "Bucket Name", key: "bucket_name" },
      { title: "Prefix", key: "prefix" },
      { title: "Depth", key: "depth" },
    ];

    const onCrudCreate = postMinioStorage;
    const onCrudGet = getMinioStorages;
    const onCrudGetTotal = getMinioTotalStorages;
    const onCrudUpdate = putMinioStorage;
    const onCrudDelete = deleteMinioStorage;

    function onOpenEditor() {
      load();
    }

    function onCloseEditor() {
      table.row = {
        category: undefined,
        name: undefined,
        endpoint: undefined,
        bucket_name: undefined,
        prefix: undefined,
        depth: undefined,
        access_key: undefined,
        secret_key: undefined,
      };
      reset(categoriesDropdown);
      reset(bucketsDropdown);
    }

    return {
      table,
      headers,
      categoriesDropdown,
      bucketsDropdown,
      prefix,
      onSelectCategory,
      onSelectBucket,
      onCrudCreate,
      onCrudGet,
      onCrudGetTotal,
      onCrudUpdate,
      onCrudDelete,
      onOpenEditor,
      onCloseEditor,
    };
  },
};
</script>
