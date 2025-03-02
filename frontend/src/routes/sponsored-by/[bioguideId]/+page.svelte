<script lang="ts">
import { onMount } from 'svelte';
import type { PageProps } from './$types';
import SearchResult from '$lib/searchResult.svelte';

let { data }: PageProps = $props();

let pd = $state(undefined);

onMount(async () => {
  pd = await (await fetch(`http://localhost:5000/member?bioguideId=${data.bioguideId}`)).json();
});
</script>

<header class="bg-linear-to-br from-indigo-800 to-purple-900 py-6 px-2">
  <h1 class="text-2xl max-w-[1000px] mx-auto my-8 font-bold text-white">
    {pd === undefined ? "Loading..." : `Bills Sponsored by ${pd.member.fullName}`}
  </h1>
</header>

<div class="mt-8 mb-4 flex justify-center">
  <main class="max-w-[1000px] mx-4">
    {#if pd === undefined}
      <p>Loading...</p>
    {:else}
      <ul class="rounded-xl border border-gray-200 overflow-hidden divide-y divide-gray-200">
        {#each pd.bills as bill}
          <SearchResult result={bill} />
        {/each}
      </ul>
    {/if}
  </main>
</div>
