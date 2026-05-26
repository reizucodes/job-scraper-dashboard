<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    loading?: boolean;
    disabled?: boolean;
    label: string;
    variant?: "primary" | "secondary" | "danger" | "ghost";
    size?: "sm" | "md";
    fullWidth?: boolean;
    type?: "button" | "submit";
  }>(),
  {
    loading: false,
    disabled: false,
    variant: "primary",
    size: "md",
    fullWidth: false,
    type: "button",
  },
);

const classes = computed(() => {
  const base =
    "inline-flex items-center justify-center rounded-md font-medium transition disabled:cursor-not-allowed disabled:opacity-60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-100 focus-visible:ring-offset-2";
  const size = props.size === "sm" ? "px-3 py-1.5 text-xs" : "px-4 py-2 text-sm";
  const width = props.fullWidth ? "w-full" : "";

  const variantMap: Record<string, string> = {
    primary: "bg-brand-600 text-white hover:bg-brand-700",
    secondary: "bg-slate-200 text-slate-800 hover:bg-slate-300",
    danger: "bg-red-600 text-white hover:bg-red-700",
    ghost: "bg-transparent text-slate-700 hover:bg-slate-100",
  };

  return [base, size, width, variantMap[props.variant]].join(" ");
});
</script>

<template>
  <button :type="type" :disabled="disabled || loading" :aria-busy="loading" :class="classes">
    {{ loading ? "Working..." : label }}
  </button>
</template>
