<script lang="ts">
import type { PageProps } from './$types';
import SearchResult from '$lib/searchResult.svelte';

let { data }: PageProps = $props();
</script>

<header class="bg-purple-200 py-6 px-2">
  <h1 class="text-2xl max-w-[1000px] mx-auto px-4 font-bold">Bills Sponsored by {data.member.fullName}</h1>
</header>

<main class="max-w-[1000px] mt-8 mx-auto px-4 pb-4">
  <ul class="rounded-xl border border-gray-200 overflow-hidden divide-y divide-gray-200">
    {#each data.bills as bill}
      <SearchResult result={bill} />
    {/each}
  </ul>
</main>
