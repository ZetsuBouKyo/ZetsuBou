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
import SettingTag from "./views/Vertical/Settings/Tag/TagTable.vue";
import SettingTagAttribute from "./views/Vertical/Settings/Tag/TagAttributeTable.vue";
import SettingTagFrontUI from "./views/Vertical/Settings/Tag/FrontUI/index.vue";
import SettingTagToken from "./views/Vertical/Settings/Tag/TagTokenTable.vue";
import Vertical from "./views/Vertical/index.vue";
import Video from "./views/Vertical/Video/index.vue";
import Videos from "./views/Vertical/Videos.vue";

/** @type {import('vue-router').RouterOptions['routes']} */

export const routes = [
  {
    path: "/",
    component: Vertical,
    children: [
      { path: "/", component: Galleries, meta: { title: "Home" } },
      {
        path: "/bookmark",
        component: Bookmark,
        meta: { title: "Bookmark" },
        children: [
          { path: "gallery", component: BookmarkGallery, meta: { title: "Gallery Bookmark" } },
          { path: "video", component: BookmarkVideo, meta: { title: "Video Bookmark" } },
        ],
      },
      { path: "/gallery", component: Galleries, meta: { title: "Gallery" } },
      { path: "/gallery/random", component: Galleries, meta: { title: "Gallery Random" } },
      { path: "/gallery/search", component: Galleries, meta: { title: "Gallery Search" } },
      { path: "/gallery/advanced-search", component: Galleries, meta: { title: "Gallery Advanced Search" } },
      { path: "/video", component: Videos, meta: { title: "Video" } },
      { path: "/video/random", component: Videos, meta: { title: "Video Random" } },
      { path: "/video/search", component: Videos, meta: { title: "Video Search" } },
      { path: "/video/advanced-search", component: Videos, meta: { title: "Video Advanced Search" } },
      {
        path: "/settings",
        component: Settings,
        meta: { title: "Settings" },
        children: [
          { path: "account", component: SettingAccount, meta: { title: "Account" } },
          { path: "appearance", component: SettingAppearance, meta: { title: "Appearance" } },
          { path: "authentication", component: SettingAuthentication, meta: { title: "Authentication" } },
          { path: "storage-minio", component: SettingStorageMinioTable, meta: { title: "Storage Minio" } },
          { path: "elasticsearch-count", component: SettingElasticsearchCount, meta: { title: "Elasticsearch Count" } },
          {
            path: "elasticsearch-search",
            component: SettingElasticsearchSearch,
            meta: { title: "Elasticsearch Search" },
          },
          { path: "tag", component: SettingTag, meta: { title: "Tag" } },
          { path: "tag-token", component: SettingTagToken, meta: { title: "Tag Token" } },
          { path: "tag-attribute", component: SettingTagAttribute, meta: { title: "Tag Attribute" } },
          { path: "tag-front-ui", component: SettingTagFrontUI, meta: { title: "Tag Front UI" } },
          { path: "quest", component: SettingQuest, meta: { title: "Quest" } },
          {
            path: "elasticsearch-count-quest",
            component: SettingElasticsearchCountQuest,
            meta: { title: "Elasticsearch Count Quest" },
          },
          { path: "group", component: SettingGroup, meta: { title: "Group" } },
        ],
      },
      { path: "/NotFound", component: NotFound },
      { path: "/construction", component: Construction },
      { path: "/g/:gallery", component: Gallery },
      { path: "/g/:gallery/i/:img", component: ImgSvgPreview },
      { path: "/v/:video", component: Video },
    ],
  },
  { path: "/initialization", component: Initialization, meta: { title: "Initialization" } },
  { path: "/login", component: Login, meta: { title: "Login" } },
];
