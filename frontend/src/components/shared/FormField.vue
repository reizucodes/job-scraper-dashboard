<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  label: string;
  inputId: string;
  error?: string;
  hint?: string;
}>();

const messageId = computed(() => `${props.inputId}-message`);
const hasMessage = computed(() => Boolean(props.error || props.hint));
</script>

<template>
  <div class="flex flex-col gap-1">
    <label :for="inputId" class="text-sm font-medium text-slate-700">{{ label }}</label>
    <slot :describedBy="hasMessage ? messageId : undefined" />
    <small v-if="error" :id="messageId" class="text-xs text-red-600">{{ error }}</small>
    <small v-else-if="hint" :id="messageId" class="text-xs text-slate-500">{{ hint }}</small>
  </div>
</template>
