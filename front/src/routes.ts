import { SearchCategory, SearchBase } from "@/interface/search";

import Bookmark from "./views/Vertical/Bookmark/index.vue";
import BookmarkGallery from "./views/Vertical/Bookmark/Gallery.vue";
import BookmarkVideo from "./views/Vertical/Bookmark/Video.vue";
import Construction from "./views/Vertical/Construction.vue";
import Galleries from "./views/Vertical/Galleries.vue";
import Gallery from "./views/Vertical/Gallery/index.vue";
import ImgSvgPreview from "./views/Vertical/ImgSvgPreview/index.vue";
import Initialization from "./views/Vertical/Initialization/index.vue";
import Login from "./views/Login.vue";
import NotFound from "./views/Vertical/NotFound.vue";
import SettingAccount from "./views/Vertical/Settings/Account/index.vue";
import SettingAppearance from "./views/Vertical/Settings/Appearance/index.vue";
import SettingAuthentication from "./views/Vertical/Settings/Authentication/index.vue";
import SettingElasticsearchCount from "./views/Vertical/Settings/Elasticsearch/CountTable.vue";
import SettingElasticsearchCountQuest from "./views/Vertical/Settings/Quest/ElasticsearchCountQuestTable.vue";
import SettingElasticsearchSearch from "./views/Vertical/Settings/Elasticsearch/SearchTable.vue";
import SettingGroup from "./views/Vertical/Settings/Group/GroupTable.vue";
import SettingQuest from "./views/Vertical/Settings/Quest/QuestTable.vue";
import Settings from "./views/Vertical/Settings/index.vue";
import SettingStorageMinioTable from "./views/Vertical/Settings/Storage/StorageMinioTable.vue";
import SettingSystem from "./views/Vertical/Settings/System/index.vue";
import SettingTag from "./views/Vertical/Settings/Tag/TagTable.vue";
import SettingTagAttribute from "./views/Vertical/Settings/Tag/TagAttributeTable.vue";
import SettingTagFrontUI from "./views/Vertical/Settings/Tag/FrontUI/index.vue";
import SettingTagToken from "./views/Vertical/Settings/Tag/TagTokenTable.vue";
import SettingUsers from "./views/Vertical/Settings/Users/index.vue";
import Vertical from "./views/Vertical/index.vue";
import Video from "./views/Vertical/Video/index.vue";
import Videos from "./views/Vertical/Videos.vue";
/** @type {import('vue-router').RouterOptions['routes']} */

import { galleryState } from "@/state/gallery";
import { settingState } from "@/state/Setting/front";
import { userState } from "@/state/user";
import { videoState } from "@/state/video";

export const routes = [
  {
    path: "/",
    component: Vertical,
    children: [
      {
        path: "/",
        component: Galleries,
        meta: { title: "Home", search: SearchCategory.Gallery, base: SearchBase.Search },
      },
      {
        path: "/bookmark",
        component: Bookmark,
        meta: { title: "Bookmark" },
        children: [
          { path: "gallery", component: BookmarkGallery, meta: { title: "Gallery Bookmark" } },
          { path: "video", component: BookmarkVideo, meta: { title: "Video Bookmark" } },
        ],
      },
      {
        path: "/gallery",
        component: Galleries,
        meta: { title: "Gallery", search: SearchCategory.Gallery, base: SearchBase.Search },
        children: [
          { path: "random", component: Galleries, meta: { title: "Gallery Random", base: SearchBase.Random } },
          { path: "search", component: Galleries, meta: { title: "Gallery Search", base: SearchBase.Search } },
          {
            path: "advanced-search",
            component: Galleries,
            meta: { title: "Gallery Advanced Search" },
          },
        ],
      },
      {
        path: "/g/:gallery",
        component: Gallery,
        meta: { title: "Gallery", search: SearchCategory.Gallery, base: SearchBase.Search },
        beforeEnter: (to: any, from: any, next: any) => {
          const id = to.params.gallery as string;
          galleryState.init(id).then(() => next());
        },
      },
      {
        path: "/g/:gallery/i/:img",
        component: ImgSvgPreview,
        meta: { title: "Gallery", search: SearchCategory.Gallery, base: SearchBase.Search },
      },
      {
        path: "/video",
        component: Videos,
        meta: { title: "Video", search: SearchCategory.Video, base: SearchBase.Search },
        children: [
          { path: "random", component: Videos, meta: { title: "Video Random", base: SearchBase.Random } },
          { path: "search", component: Videos, meta: { title: "Video Search", base: SearchBase.Search } },
          { path: "advanced-search", component: Videos, meta: { title: "Video Advanced Search" } },
        ],
      },
      {
        path: "/v/:video",
        component: Video,
        meta: { title: "Video", search: SearchCategory.Video, base: SearchBase.Search },
        beforeEnter: (to: any, from: any, next: any) => {
          const id = to.params.video as string;
          videoState.init(id).then(() => next());
        },
      },
      {
        path: "/settings",
        component: Settings,
        meta: { title: "Settings" },
        children: [
          { path: "account", component: SettingAccount, meta: { title: "Account" } },
          { path: "appearance", component: SettingAppearance, meta: { title: "Appearance" } },
          { path: "authentication", component: SettingAuthentication, meta: { title: "Authentication" } },
          { path: "elasticsearch-count", component: SettingElasticsearchCount, meta: { title: "Elasticsearch Count" } },
          {
            path: "elasticsearch-count-quest",
            component: SettingElasticsearchCountQuest,
            meta: { title: "Elasticsearch Count Quest" },
          },
          {
            path: "elasticsearch-search",
            component: SettingElasticsearchSearch,
            meta: { title: "Elasticsearch Search" },
          },
          { path: "group", component: SettingGroup, meta: { title: "Group" } },
          { path: "tag", component: SettingTag, meta: { title: "Tag" } },
          { path: "tag-attribute", component: SettingTagAttribute, meta: { title: "Tag Attribute" } },
          { path: "tag-front-ui", component: SettingTagFrontUI, meta: { title: "Tag Front UI" } },
          { path: "tag-token", component: SettingTagToken, meta: { title: "Tag Token" } },
          { path: "quest", component: SettingQuest, meta: { title: "Quest" } },
          { path: "storage-minio", component: SettingStorageMinioTable, meta: { title: "Storage Minio" } },
          { path: "system", component: SettingSystem, meta: { title: "System" } },
          { path: "users", component: SettingUsers, meta: { title: "Users" } },
        ],
      },
      { path: "/NotFound", component: NotFound },
      { path: "/construction", component: Construction },
    ],
    beforeEnter: (to: any, from: any, next: any) => {
      Promise.all([userState.init(), settingState.init()]).then(() => next());
    },
  },
  { path: "/initialization", component: Initialization, meta: { title: "Initialization" } },
  { path: "/login", component: Login, meta: { title: "Login" } },
];
