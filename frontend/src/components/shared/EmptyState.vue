<script setup lang="ts">
defineProps<{ message: string }>();
</script>

<template>
  <p class="rounded-md border border-dashed border-slate-300 bg-white px-3 py-4 text-sm text-slate-600" role="status" aria-live="polite">
    {{ message }}
  </p>
</template>
