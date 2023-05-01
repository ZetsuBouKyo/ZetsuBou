import Administration from "./views/Vertical/Administration/index.vue";
import AdministrationGroup from "./views/Vertical/Administration/Group/index.vue";
import AdministrationStorage from "./views/Vertical/Administration/Storage/index.vue";
import Count from "./views/Vertical/ElasticQuery/Count.vue";
import ElasticCountQuest from "./views/Vertical/Quest/ElasticCountQuest/index.vue";
import ElasticQuery from "./views/Vertical/ElasticQuery/index.vue";
import FrontUI from "./views/Vertical/Administration/FrontUI/index.vue";
import Galleries from "./views/Vertical/Galleries.vue";
import Gallery from "./views/Vertical/Gallery/index.vue";
import ImgSvgPreview from "./views/Vertical/ImgSvgPreview/index.vue";
import Login from "./views/Login.vue";
import NotFound from "./views/Vertical/NotFound.vue";
import Quest from "./views/Vertical/Quest/index.vue";
import QuestQuest from "./views/Vertical/Quest/Quest/index.vue";
import Search from "./views/Vertical/ElasticQuery/Search.vue";
import Tag from "./views/Vertical/Tag/index.vue";
import TagAttribute from "./views/Vertical/Tag/Attribute/index.vue";
import TagTag from "./views/Vertical/Tag/Tag/index.vue";
import TagToken from "./views/Vertical/Tag/Token/index.vue";
import Task from "./views/Vertical/Administration/Task/index.vue";
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
      { path: "/gallery", component: Galleries, meta: { title: "Gallery" } },
      { path: "/gallery/random", component: Galleries, meta: { title: "Gallery Random" } },
      { path: "/gallery/search", component: Galleries, meta: { title: "Gallery Search" } },
      { path: "/gallery/advanced-search", component: Galleries, meta: { title: "Gallery Advanced Search" } },
      { path: "/video", component: Videos, meta: { title: "Video" } },
      { path: "/video/random", component: Videos, meta: { title: "Video Random" } },
      { path: "/video/search", component: Videos, meta: { title: "Video Search" } },
      { path: "/video/advanced-search", component: Videos, meta: { title: "Video Advanced Search" } },
      {
        path: "/administration",
        component: Administration,
        meta: { title: "Administration" },
        children: [
          { path: "user", component: NotFound, meta: { title: "User" } },
          { path: "group", component: AdministrationGroup, meta: { title: "Group" } },
          { path: "storage", component: AdministrationStorage, meta: { title: "Storage" } },
          { path: "front-ui", component: FrontUI, meta: { title: "Front UI" } },
          { path: "task", component: Task, meta: { title: "Task" } },
        ],
      },
      {
        path: "/elastic-query",
        component: ElasticQuery,
        meta: { title: "ElasticQuery" },
        children: [
          { path: "count", component: Count, meta: { title: "ElasticQueryCount" } },
          { path: "search", component: Search, meta: { title: "ElasticQuerySearch" } },
        ],
      },
      {
        path: "/tag",
        component: Tag,
        meta: { title: "Tag" },
        children: [
          { path: "tag", component: TagTag, meta: { title: "Tag" } },
          { path: "token", component: TagToken, meta: { title: "Token" } },
          { path: "attribute", component: TagAttribute, meta: { title: "Attribute" } },
        ],
      },
      {
        path: "/quest",
        component: Quest,
        meta: { title: "Quest" },
        children: [
          { path: "quest", component: QuestQuest, meta: { title: "Quest" } },
          { path: "elastic-count-quest", component: ElasticCountQuest, meta: { title: "ElasticCountQuest" } },
        ],
      },
      { path: "/elastic-count-quest", component: ElasticCountQuest, meta: { title: "ElasticCountQuest" } },
      { path: "/NotFound", component: NotFound },
      { path: "/g/:gallery", component: Gallery },
      { path: "/g/:gallery/i/:img", component: ImgSvgPreview },
      { path: "/v/:video", component: Video },
    ],
  },
  { path: "/login", component: Login, meta: { title: "Login" } },
];
