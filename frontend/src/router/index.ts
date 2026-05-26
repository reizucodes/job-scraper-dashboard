import { createRouter, createWebHistory } from "vue-router";

import JobsView from "@/views/JobsView.vue";
import RunsView from "@/views/RunsView.vue";
import SourcesView from "@/views/SourcesView.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/jobs" },
    { path: "/jobs", name: "jobs", component: JobsView },
    { path: "/sources", name: "sources", component: SourcesView },
    { path: "/runs", name: "runs", component: RunsView },
  ],
});
