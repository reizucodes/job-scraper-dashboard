<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import ActionButton from "@/components/shared/ActionButton.vue";
import DataTable from "@/components/shared/DataTable.vue";
import EmptyState from "@/components/shared/EmptyState.vue";
import ErrorState from "@/components/shared/ErrorState.vue";
import LoadingState from "@/components/shared/LoadingState.vue";
import { useJobSourcesStore } from "@/stores/jobSources";
import { useScrapeRunsStore } from "@/stores/scrapeRuns";

const jobSourcesStore = useJobSourcesStore();
const scrapeRunsStore = useScrapeRunsStore();
const selectedSourceId = ref<number | null>(null);

const selectedSourceIds = computed(() => (selectedSourceId.value === null ? undefined : [selectedSourceId.value]));

onMounted(async () => {
  await jobSourcesStore.load();
  await scrapeRunsStore.load();
});
</script>

<template>
  <section class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-slate-900">Scrape Runs</h2>
      <p class="text-sm text-slate-600">Trigger synchronous runs and inspect ingestion metrics.</p>
    </div>

    <div class="flex flex-col gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-end">
      <label class="w-full text-sm font-medium text-slate-700 sm:max-w-xs" for="run-source-scope">
        Source scope
        <select id="run-source-scope" v-model.number="selectedSourceId" class="mt-1">
          <option :value="null">All enabled sources</option>
          <option v-for="source in jobSourcesStore.items" :key="source.id" :value="source.id">{{ source.name }}</option>
        </select>
      </label>
      <ActionButton label="Trigger scrape run" :loading="scrapeRunsStore.triggerStatus === 'loading'" @click="scrapeRunsStore.trigger(selectedSourceIds)" />
    </div>

    <div v-if="scrapeRunsStore.lastTrigger" class="rounded-md border border-brand-100 bg-brand-50 px-3 py-2 text-sm text-brand-700" role="status" aria-live="polite">
      Run #{{ scrapeRunsStore.lastTrigger.run_id }} {{ scrapeRunsStore.lastTrigger.status }} |
      seen {{ scrapeRunsStore.lastTrigger.metrics.records_seen }},
      inserted {{ scrapeRunsStore.lastTrigger.metrics.records_inserted }},
      updated {{ scrapeRunsStore.lastTrigger.metrics.records_updated }},
      duplicates {{ scrapeRunsStore.lastTrigger.metrics.duplicates }},
      failures {{ scrapeRunsStore.lastTrigger.metrics.failures }}
    </div>

    <LoadingState v-if="scrapeRunsStore.status === 'loading'" message="Loading runs..." />
    <ErrorState v-if="scrapeRunsStore.error" :message="scrapeRunsStore.error" />
    <EmptyState v-if="scrapeRunsStore.status === 'success' && scrapeRunsStore.items.length === 0" message="No runs yet." />

    <DataTable v-if="scrapeRunsStore.items.length > 0" caption="Scrape runs table">
      <thead class="bg-slate-50 text-xs uppercase tracking-wide text-slate-600">
        <tr>
          <th class="px-3 py-2">ID</th>
          <th class="px-3 py-2">Status</th>
          <th class="px-3 py-2">Seen</th>
          <th class="px-3 py-2">Inserted</th>
          <th class="px-3 py-2">Updated</th>
          <th class="px-3 py-2">Duplicates</th>
          <th class="px-3 py-2">Failures</th>
          <th class="px-3 py-2">Duration</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100">
        <tr v-for="run in scrapeRunsStore.items" :key="run.id">
          <td class="px-3 py-2">{{ run.id }}</td>
          <td class="px-3 py-2 font-medium">{{ run.status }}</td>
          <td class="px-3 py-2">{{ run.records_seen }}</td>
          <td class="px-3 py-2">{{ run.records_inserted }}</td>
          <td class="px-3 py-2">{{ run.records_updated }}</td>
          <td class="px-3 py-2">{{ run.duplicates }}</td>
          <td class="px-3 py-2">{{ run.failures }}</td>
          <td class="px-3 py-2">{{ run.duration_ms ?? '-' }}</td>
        </tr>
      </tbody>
    </DataTable>
  </section>
</template>
