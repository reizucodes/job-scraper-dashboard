<script setup lang="ts">
import { onMounted, ref } from "vue";

import type { BookmarkStatus, ExportFormat } from "@/api/types";
import ActionButton from "@/components/shared/ActionButton.vue";
import DataTable from "@/components/shared/DataTable.vue";
import EmptyState from "@/components/shared/EmptyState.vue";
import ErrorState from "@/components/shared/ErrorState.vue";
import LoadingState from "@/components/shared/LoadingState.vue";
import { useBookmarksStore } from "@/stores/bookmarks";
import { useExportsStore } from "@/stores/exports";
import { useJobsStore } from "@/stores/jobs";

const jobsStore = useJobsStore();
const bookmarksStore = useBookmarksStore();
const exportsStore = useExportsStore();

const titleQuery = ref("");
const location = ref("");
const workMode = ref("");
const exportFormat = ref<ExportFormat>("csv");
const filterFeedback = ref("");

async function applyFilters(): Promise<void> {
  jobsStore.setFilters({
    title_query: titleQuery.value || undefined,
    location: location.value || undefined,
    work_mode: workMode.value || undefined,
  });
  await jobsStore.load();
  filterFeedback.value = `Loaded ${jobsStore.items.length} jobs`;
}

async function updateBookmark(jobId: number, status: BookmarkStatus): Promise<void> {
  const updatedStatus = await bookmarksStore.setStatus(jobId, status);
  const item = jobsStore.items.find((job) => job.id === jobId);
  if (item) {
    item.bookmark_status = updatedStatus;
  }
}

async function runExport(): Promise<void> {
  await exportsStore.run(exportFormat.value, jobsStore.filters);
}

onMounted(async () => {
  await jobsStore.load();
  filterFeedback.value = `Loaded ${jobsStore.items.length} jobs`;
});
</script>

<template>
  <section class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-slate-900">Job Listings</h2>
      <p class="text-sm text-slate-600">Filter, bookmark, and export normalized job listings.</p>
    </div>

    <div class="grid gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm sm:grid-cols-4">
      <label class="sr-only" for="jobs-title-filter">Title filter</label>
      <input id="jobs-title-filter" v-model="titleQuery" placeholder="Title filter" />

      <label class="sr-only" for="jobs-location-filter">Location filter</label>
      <input id="jobs-location-filter" v-model="location" placeholder="Location filter" />

      <label class="sr-only" for="jobs-mode-filter">Work mode filter</label>
      <select id="jobs-mode-filter" v-model="workMode">
        <option value="">Any mode</option>
        <option value="remote">Remote</option>
        <option value="hybrid">Hybrid</option>
        <option value="onsite">Onsite</option>
      </select>

      <ActionButton data-testid="apply-filters" label="Apply filters" @click="applyFilters" />
    </div>

    <p v-if="filterFeedback" class="rounded-md bg-slate-100 px-3 py-2 text-sm text-slate-700" role="status" aria-live="polite">{{ filterFeedback }}</p>

    <div class="flex flex-col gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center">
      <label class="sr-only" for="jobs-export-format">Export format</label>
      <select id="jobs-export-format" v-model="exportFormat" class="sm:max-w-[10rem]">
        <option value="csv">CSV</option>
        <option value="xlsx">XLSX</option>
      </select>
      <ActionButton data-testid="run-export" label="Export filtered jobs" :loading="exportsStore.status === 'loading'" @click="runExport" />
      <span v-if="exportsStore.lastFilename" class="text-sm text-emerald-700" role="status" aria-live="polite">Saved: {{ exportsStore.lastFilename }}</span>
    </div>
    <ErrorState v-if="exportsStore.error" :message="exportsStore.error" />

    <LoadingState v-if="jobsStore.status === 'loading'" message="Loading jobs..." />
    <ErrorState v-if="jobsStore.error" :message="jobsStore.error" />
    <EmptyState v-if="jobsStore.status === 'success' && jobsStore.items.length === 0" message="No jobs match filters." />

    <DataTable v-if="jobsStore.items.length > 0" caption="Job listings table">
      <thead class="bg-slate-50 text-xs uppercase tracking-wide text-slate-600">
        <tr>
          <th class="px-3 py-2">Title</th>
          <th class="px-3 py-2">Company</th>
          <th class="px-3 py-2">Location</th>
          <th class="px-3 py-2">Work Mode</th>
          <th class="px-3 py-2">Skills</th>
          <th class="px-3 py-2">Bookmark</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100">
        <tr v-for="job in jobsStore.items" :key="job.id">
          <td class="px-3 py-2 font-medium">
            <a
              :href="job.apply_url"
              class="text-slate-900 underline decoration-slate-300 underline-offset-2 hover:text-brand-700 hover:decoration-brand-400"
              rel="noreferrer noopener"
              target="_blank"
            >
              {{ job.title }}
            </a>
          </td>
          <td class="px-3 py-2">{{ job.company }}</td>
          <td class="px-3 py-2">{{ job.location ?? '-' }}</td>
          <td class="px-3 py-2">{{ job.work_mode ?? '-' }}</td>
          <td class="px-3 py-2 text-slate-600">{{ job.skills.join(', ') }}</td>
          <td class="px-3 py-2">
            <label class="sr-only" :for="`bookmark-${job.id}`">Bookmark status</label>
            <select
              :id="`bookmark-${job.id}`"
              data-testid="bookmark-select"
              :value="job.bookmark_status"
              @change="updateBookmark(job.id, ($event.target as HTMLSelectElement).value as BookmarkStatus)"
            >
              <option value="new">new</option>
              <option value="interested">interested</option>
              <option value="applied">applied</option>
              <option value="rejected">rejected</option>
            </select>
          </td>
        </tr>
      </tbody>
    </DataTable>
  </section>
</template>
