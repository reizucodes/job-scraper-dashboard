<script setup lang="ts">
defineProps<{ message?: string }>();
</script>

<template>
  <p class="rounded-md border border-slate-200 bg-slate-100 px-3 py-2 text-sm text-slate-700" role="status" aria-live="polite">
    {{ message ?? "Loading..." }}
  </p>
</template>
