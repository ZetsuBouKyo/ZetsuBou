<template>
  <div class="views-setting-container">
    <crud-table
      class="w-full"
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
      :on-close-editor="onCloseEditor">
      <template v-slot:buttons="slot">
        <crud-table-button :text="'Sync'" :color="ButtonColorEnum.Primary" :row="slot.row" :onClick="sync">
          <template v-slot:icon><icon-mdi-file-edit-outline /></template>
        </crud-table-button>
      </template>
      <template v-slot:editor>
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
            autocomplete="new-password" />
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Access key:</span>
          <input
            class="flex-1 modal-input"
            type="password"
            :placeholder="table.row.access_key"
            v-model="table.row.access_key"
            autocomplete="new-password" />
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Secret key:</span>
          <input
            class="flex-1 modal-input"
            type="password"
            :placeholder="table.row.secret_key"
            v-model="table.row.secret_key"
            autocomplete="new-password" />
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Category:</span>
          <select-dropdown
            class="h-10 w-64"
            :options-width-class="'w-64'"
            :state="categoriesDropdown"
            :on-select="onSelectCategory"></select-dropdown>
        </div>
        <div class="modal-row">
          <span class="w-32 mr-4">Bucket Name:</span>
          <select-dropdown
            class="h-10 w-64"
            :options-width-class="'w-64'"
            :state="bucketsDropdown"
            :on-select="onSelectBucket"></select-dropdown>
          <span class="ml-4 text-blue-500" v-if="table.connected === ConnectionStatus.Connected">Connected</span>
          <span class="ml-4 text-yellow-500" v-else-if="table.connected === ConnectionStatus.Connecting"
            >Connecting</span
          >
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
            @click="updatePrefixes" />
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
            v-model="table.row.depth" />
          <datalist id="admin-minio-storage-depth">
            <option v-for="(p, i) in [1, 2, 3, 4, 5, 6, 7]" :value="p" :key="i" />
          </datalist>
        </div>
      </template>
      <template v-slot:editor-buttons>
        <button class="flex ml-2 btn btn-primary" @click="checkConnection()">Check Connection</button>
      </template>
    </crud-table>
  </div>
</template>

<script lang="ts">
import { reactive, watch } from "vue";

import { getStorageMinioList } from "@/api/v1/storage/minio/operation";
import {
  deleteStorageMinio,
  getStorageMinioCategories,
  getStorageMinioTotalStorages,
  getStorageMinios,
  postStorageMinio,
  putStorageMinio,
} from "@/api/v1/storage/minio/storage";
import { postSyncStorageMinio } from "@/api/v1/task/airflow";

import { ButtonColorEnum } from "@/elements/Button/button";
import SelectDropdown, { SelectDropdownState, reset } from "@/elements/Dropdown/SelectDropdown.vue";
import CrudTableButton from "@/elements/Table/CrudTable/CrudTableButton.vue";
import CrudTable, { CrudTableState, Header } from "@/elements/Table/CrudTable/index.vue";

import { messageState } from "@/state/message";

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

interface GetStorageMinioListParams {
  bucket_name?: string;
  prefix?: string;
  endpoint: string;
  access_key: string;
  secret_key: string;
}

enum ConnectionStatus {
  Connected = 1,
  Failed = 0,
  Connecting = -1,
}

export default {
  components: { CrudTable, CrudTableButton, SelectDropdown },
  setup() {
    const table = CrudTable.initState() as CrudTableState<Row>;
    table.connected = ConnectionStatus.Failed;

    const prefix = reactive({
      options: [],
    });

    const bucketsDropdown = SelectDropdown.initState() as SelectDropdownState;
    const categoriesDropdown = SelectDropdown.initState() as SelectDropdownState;

    function updateOptions(params) {
      if (table.connected === ConnectionStatus.Connecting) {
        return;
      }
      table.connected = ConnectionStatus.Connecting;
      return getStorageMinioList(params)
        .then((response) => {
          const s3Objects = response.data;
          if (response.status !== 200) {
            minioConnectError();
            return;
          }
          prefix.options = [];
          table.connected = ConnectionStatus.Connected;
          if (s3Objects) {
            for (const s3Object of s3Objects) {
              if (s3Object.prefix.slice(-1) === "/") {
                prefix.options.push(s3Object.prefix);
              }
              bucketsDropdown.options.push({ title: s3Object.bucket_name, value: s3Object.bucket_name });
            }
          }
        })
        .catch(() => {
          minioConnectError();
        });
    }

    function updatePrefixes() {
      const bucketName = table.row.bucket_name;
      if (!bucketName) {
        return;
      }
      let prefix = table.row.prefix;

      if (!prefix) {
        prefix = "";
      } else if (!prefix.endsWith("/")) {
        return;
      }

      const params: GetStorageMinioListParams = {
        bucket_name: bucketName,
        prefix: prefix,
        endpoint: table.row.endpoint,
        access_key: table.row.access_key,
        secret_key: table.row.secret_key,
      };

      updateOptions(params);
    }

    function getPrefixAutoComplete(bucketName: string, prefixName: string) {
      prefix.options = [];

      if (!bucketName) {
        return;
      }
      if (!table.row.endpoint || !table.row.access_key || !table.row.secret_key) {
        return;
      }

      const params: GetStorageMinioListParams = {
        endpoint: table.row.endpoint,
        access_key: table.row.access_key,
        secret_key: table.row.secret_key,
      };
      params.bucket_name = bucketName;
      if (prefixName) {
        params.prefix = prefixName;
      }

      updateOptions(params);
    }

    function checkConnection() {
      const params = {
        endpoint: table.row.endpoint,
        access_key: table.row.access_key,
        secret_key: table.row.secret_key,
      };
      updateOptions(params);
    }

    watch(
      () => {
        if (!table.row) {
          return undefined;
        }
        return table.row.prefix;
      },
      () => {
        const bucketName = bucketsDropdown.selectedValue as string;
        let prefixName = table.row.prefix as string;
        if (table.connected !== ConnectionStatus.Connected || bucketName === undefined) {
          return;
        }

        if (prefixName === undefined) {
          prefixName = "";
        }

        if (prefixName.slice(-1) === "/" || !prefixName) {
          getPrefixAutoComplete(bucketName, prefixName);
        }
      },
    );

    function minioConnectError() {
      bucketsDropdown.options = [];
      prefix.options = [];
      table.row.prefix = undefined;
      table.row.bucket_name = undefined;
      table.connected = ConnectionStatus.Failed;
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
        return undefined;
      },
      (status, _) => {
        if (!status) {
          return;
        }
        checkConnection();
      },
    );

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
    getStorageMinioCategories().then((response) => {
      const data = response.data;
      if (data) {
        for (let key in data) {
          categories[data[key]] = key;
        }
      }
    });

    function load() {
      getStorageMinioCategories().then((response) => {
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

    const onCrudCreate = postStorageMinio;
    const onCrudGet = getStorageMinios;
    const onCrudGetTotal = getStorageMinioTotalStorages;
    const onCrudUpdate = putStorageMinio;
    const onCrudDelete = deleteStorageMinio;

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
      table.connected = ConnectionStatus.Failed;
      reset(categoriesDropdown);
      reset(bucketsDropdown);
    }

    function sync(row: Row) {
      if (row === undefined || row.id === undefined) {
        return;
      }
      const id = row.id;
      postSyncStorageMinio(id).then((response: any) => {
        messageState.sendAirflowMessage(
          response,
          `Synchronizing storage: ${id}`,
          `Successfully synchronized storage: ${id}`,
          "Failed to synchronize",
        );
      });
    }

    return {
      bucketsDropdown,
      ButtonColorEnum,
      categoriesDropdown,
      checkConnection,
      ConnectionStatus,
      headers,
      onCloseEditor,
      onCrudCreate,
      onCrudDelete,
      onCrudGet,
      onCrudGetTotal,
      onCrudUpdate,
      onOpenEditor,
      onSelectBucket,
      onSelectCategory,
      prefix,
      sync,
      table,
      updatePrefixes,
    };
  },
};
</script>
