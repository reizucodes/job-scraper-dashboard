<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import ActionButton from "@/components/shared/ActionButton.vue";
import DataTable from "@/components/shared/DataTable.vue";
import EmptyState from "@/components/shared/EmptyState.vue";
import ErrorState from "@/components/shared/ErrorState.vue";
import FormField from "@/components/shared/FormField.vue";
import LoadingState from "@/components/shared/LoadingState.vue";
import type { JobSourceConfig, JobSourceConfigMode, JobSourceDto } from "@/api/types";
import { useJobSourcesStore } from "@/stores/jobSources";
import { useSourceProfilesStore } from "@/stores/sourceProfiles";

const sourceProfilesStore = useSourceProfilesStore();
const jobSourcesStore = useJobSourcesStore();

const form = ref({
  name: "",
  base_url: "",
  profile_id: 0,
  enabled: true,
  mode: "fixture" as JobSourceConfigMode,
  jobs_url: "",
  user_agent: "",
  timeout_seconds: "",
  fixtures_json: "",
});
const editingId = ref<number | null>(null);
const submitting = ref(false);
const feedback = ref("");
const formError = ref("");

const nameError = computed(() => (form.value.name.trim() ? "" : "Name is required"));
const urlError = computed(() => (/^https?:\/\//.test(form.value.base_url) ? "" : "Valid URL required"));
const profileError = computed(() => (form.value.profile_id > 0 ? "" : "Choose a profile"));
const jobsUrlError = computed(() => (form.value.mode === "live" && !form.value.jobs_url.trim() ? "jobs_url is required for live mode" : ""));
const fixtureJsonError = computed(() => {
  if (form.value.mode !== "fixture" || !form.value.fixtures_json.trim()) return "";
  try {
    const parsed = JSON.parse(form.value.fixtures_json);
    if (!Array.isArray(parsed) || !parsed.every((item) => item !== null && typeof item === "object" && !Array.isArray(item))) {
      return "Fixture JSON must be an array of objects";
    }
    return "";
  } catch {
    return "Fixture JSON must be valid JSON";
  }
});
const canSubmit = computed(
  () => !nameError.value && !urlError.value && !profileError.value && !jobsUrlError.value && !fixtureJsonError.value,
);
const selectedProfile = computed(() => sourceProfilesStore.items.find((profile) => profile.id === form.value.profile_id) ?? null);
const profileHelperText = computed(() => {
  if (selectedProfile.value?.code === "greenhouse") {
    return "Expected live URL: https://boards-api.greenhouse.io/v1/boards/<board_token>/jobs";
  }
  if (selectedProfile.value?.code === "lever") {
    return "Expected live URL: https://api.lever.co/v0/postings/<company>?mode=json";
  }
  return "Custom HTML uses shared/basic config only in MVP.";
});

async function submitSource(): Promise<void> {
  if (!canSubmit.value) return;
  submitting.value = true;
  feedback.value = "";
  formError.value = "";
  try {
    const payload = {
      name: form.value.name,
      base_url: form.value.base_url,
      profile_id: form.value.profile_id,
      enabled: form.value.enabled,
      config: toConfigPayload(),
    };
    if (editingId.value === null) {
      await jobSourcesStore.create(payload);
      feedback.value = "Source created";
    } else {
      await jobSourcesStore.update(editingId.value, payload);
      feedback.value = "Source updated";
    }
    resetForm();
  } catch {
    formError.value = jobSourcesStore.error || "Failed to save source";
  } finally {
    submitting.value = false;
  }
}

async function toggleEnabled(id: number, enabled: boolean): Promise<void> {
  feedback.value = "";
  await jobSourcesStore.update(id, { enabled: !enabled });
  feedback.value = "Source updated";
}

async function removeSource(id: number): Promise<void> {
  feedback.value = "";
  await jobSourcesStore.remove(id);
  feedback.value = "Source deleted";
  if (editingId.value === id) {
    resetForm();
  }
}

function editSource(source: JobSourceDto): void {
  const config = source.config ?? {};
  const mode = config.mode === "live" ? "live" : "fixture";
  const fixtures = Array.isArray(config.fixtures) ? config.fixtures : [];
  editingId.value = source.id;
  formError.value = "";
  feedback.value = "";
  form.value.name = source.name;
  form.value.base_url = source.base_url;
  form.value.profile_id = source.profile_id;
  form.value.enabled = source.enabled;
  form.value.mode = mode;
  form.value.jobs_url = typeof config.jobs_url === "string" ? config.jobs_url : "";
  form.value.user_agent = typeof config.user_agent === "string" ? config.user_agent : "";
  form.value.timeout_seconds = typeof config.timeout_seconds === "number" ? String(config.timeout_seconds) : "";
  form.value.fixtures_json = fixtures.length > 0 ? JSON.stringify(fixtures, null, 2) : "";
}

function cancelEdit(): void {
  resetForm();
}

function toConfigPayload(): JobSourceConfig {
  const timeout = form.value.timeout_seconds.trim() ? Number(form.value.timeout_seconds) : undefined;
  const base: JobSourceConfig = {
    mode: form.value.mode,
  };
  if (form.value.user_agent.trim()) {
    base.user_agent = form.value.user_agent.trim();
  }
  if (timeout !== undefined && Number.isFinite(timeout)) {
    base.timeout_seconds = timeout;
  }

  if (form.value.mode === "live") {
    base.jobs_url = form.value.jobs_url.trim();
    return base;
  }

  if (!form.value.fixtures_json.trim()) {
    base.fixtures = [];
    return base;
  }
  base.fixtures = JSON.parse(form.value.fixtures_json) as Array<Record<string, unknown>>;
  return base;
}

function resetForm(): void {
  const defaultProfileId = sourceProfilesStore.items.length > 0 ? sourceProfilesStore.items[0].id : 0;
  editingId.value = null;
  formError.value = "";
  form.value = {
    name: "",
    base_url: "",
    profile_id: defaultProfileId,
    enabled: true,
    mode: "fixture",
    jobs_url: "",
    user_agent: "",
    timeout_seconds: "",
    fixtures_json: "",
  };
}

onMounted(async () => {
  await sourceProfilesStore.load();
  await jobSourcesStore.load();
  resetForm();
});
</script>

<template>
  <section class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-slate-900">Sources</h2>
      <p class="text-sm text-slate-600">Manage source profiles and job source endpoints.</p>
    </div>

    <LoadingState v-if="sourceProfilesStore.status === 'loading'" message="Loading profiles..." />
    <ErrorState v-if="sourceProfilesStore.error" :message="sourceProfilesStore.error" />

    <form class="grid gap-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm sm:grid-cols-2" @submit.prevent="submitSource">
      <FormField label="Name" input-id="source-name" :error="nameError">
        <template #default="slotProps">
          <input id="source-name" v-model="form.name" :aria-describedby="slotProps.describedBy" autocomplete="off" placeholder="Source name" />
        </template>
      </FormField>

      <FormField label="Base URL" input-id="source-base-url" :error="urlError">
        <template #default="slotProps">
          <input id="source-base-url" v-model="form.base_url" :aria-describedby="slotProps.describedBy" autocomplete="off" placeholder="https://example.com/jobs" />
        </template>
      </FormField>

      <FormField class="sm:col-span-2" label="Profile" input-id="source-profile" :error="profileError">
        <template #default="slotProps">
          <select id="source-profile" v-model.number="form.profile_id" :aria-describedby="slotProps.describedBy">
            <option v-for="profile in sourceProfilesStore.items" :key="profile.id" :value="profile.id">
              {{ profile.display_name }}
            </option>
          </select>
        </template>
      </FormField>

      <FormField class="sm:col-span-2" label="Config Mode" input-id="source-config-mode">
        <template #default>
          <select id="source-config-mode" v-model="form.mode">
            <option value="fixture">fixture</option>
            <option value="live">live</option>
          </select>
        </template>
      </FormField>

      <p class="sm:col-span-2 rounded-md bg-slate-50 px-3 py-2 text-xs text-slate-700">{{ profileHelperText }}</p>

      <template v-if="form.mode === 'live'">
        <FormField class="sm:col-span-2" label="Jobs URL" input-id="source-jobs-url" :error="jobsUrlError">
          <template #default="slotProps">
            <input
              id="source-jobs-url"
              v-model="form.jobs_url"
              :aria-describedby="slotProps.describedBy"
              autocomplete="off"
              placeholder="https://provider.example/jobs"
            />
          </template>
        </FormField>
      </template>

      <template v-else>
        <FormField class="sm:col-span-2" label="Fixture JSON" input-id="source-fixtures-json" :error="fixtureJsonError">
          <template #default="slotProps">
            <textarea
              id="source-fixtures-json"
              v-model="form.fixtures_json"
              :aria-describedby="slotProps.describedBy"
              rows="6"
              placeholder='[{"id":"job-1","title":"Python Engineer"}]'
            />
          </template>
        </FormField>
      </template>

      <FormField label="User Agent (optional)" input-id="source-user-agent">
        <template #default>
          <input id="source-user-agent" v-model="form.user_agent" autocomplete="off" placeholder="job-scraper-dashboard/1.0" />
        </template>
      </FormField>

      <FormField label="Timeout Seconds (optional)" input-id="source-timeout">
        <template #default>
          <input id="source-timeout" v-model="form.timeout_seconds" type="number" min="1" max="30" placeholder="10" />
        </template>
      </FormField>

      <label class="inline-flex items-center gap-2 text-sm text-slate-700 sm:col-span-2" for="source-enabled">
        <input id="source-enabled" v-model="form.enabled" class="h-4 w-4" type="checkbox" />
        Enabled
      </label>

      <div class="sm:col-span-2">
        <div class="flex flex-wrap gap-2">
          <ActionButton :type="'submit'" :label="editingId === null ? 'Create source' : 'Update source'" :disabled="!canSubmit" :loading="submitting" />
          <ActionButton
            v-if="editingId !== null"
            :type="'button'"
            label="Cancel edit"
            variant="secondary"
            @click="cancelEdit"
          />
        </div>
      </div>
    </form>

    <p v-if="feedback" class="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-700" role="status" aria-live="polite">{{ feedback }}</p>
    <ErrorState v-if="formError" :message="formError" />
    <LoadingState v-if="jobSourcesStore.status === 'loading'" message="Loading sources..." />
    <ErrorState v-if="jobSourcesStore.error" :message="jobSourcesStore.error" />
    <EmptyState v-if="jobSourcesStore.status === 'success' && jobSourcesStore.items.length === 0" message="No sources yet." />

    <DataTable v-if="jobSourcesStore.items.length > 0" caption="Job sources table">
      <thead class="bg-slate-50 text-xs uppercase tracking-wide text-slate-600">
        <tr>
          <th class="px-3 py-2">ID</th>
          <th class="px-3 py-2">Name</th>
          <th class="px-3 py-2">URL</th>
          <th class="px-3 py-2">Profile</th>
          <th class="px-3 py-2">Enabled</th>
          <th class="px-3 py-2">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-100">
        <tr v-for="source in jobSourcesStore.items" :key="source.id" class="align-top">
          <td class="px-3 py-2">{{ source.id }}</td>
          <td class="px-3 py-2 font-medium">{{ source.name }}</td>
          <td class="px-3 py-2 break-all text-slate-600">{{ source.base_url }}</td>
          <td class="px-3 py-2">{{ sourceProfilesStore.items.find((profile) => profile.id === source.profile_id)?.display_name ?? source.profile_id }}</td>
          <td class="px-3 py-2">{{ source.enabled }}</td>
          <td class="px-3 py-2">
            <div class="flex flex-wrap gap-2">
              <ActionButton label="Edit" size="sm" variant="secondary" @click="editSource(source)" />
              <ActionButton :label="source.enabled ? 'Disable' : 'Enable'" size="sm" variant="secondary" @click="toggleEnabled(source.id, source.enabled)" />
              <ActionButton label="Delete" size="sm" variant="danger" @click="removeSource(source.id)" />
            </div>
          </td>
        </tr>
      </tbody>
    </DataTable>
  </section>
</template>
