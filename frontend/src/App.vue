<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:rounded focus:bg-white focus:px-3 focus:py-2 focus:shadow">
      Skip to main content
    </a>

    <header class="border-b border-slate-200 bg-white">
      <div class="mx-auto flex w-full max-w-6xl flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 class="text-xl font-semibold tracking-tight text-slate-900">Job Scraper Dashboard</h1>
        <nav aria-label="Primary navigation" class="flex items-center gap-2 rounded-lg bg-slate-100 p-1 text-sm">
          <RouterLink class="rounded-md px-3 py-2 text-slate-700 hover:bg-white hover:text-slate-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-100" to="/sources">Sources</RouterLink>
          <RouterLink class="rounded-md px-3 py-2 text-slate-700 hover:bg-white hover:text-slate-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-100" to="/runs">Runs</RouterLink>
          <RouterLink class="rounded-md px-3 py-2 text-slate-700 hover:bg-white hover:text-slate-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-100" to="/jobs">Jobs</RouterLink>
        </nav>
      </div>
    </header>

    <main id="main-content" class="mx-auto w-full max-w-6xl px-4 py-6">
      <RouterView />
    </main>
  </div>
</template>
