<script lang="ts">
import { onMount } from 'svelte';
import type { PageProps } from './$types';
import Header from '$lib/header.svelte';
import SearchResult from '$lib/searchResult.svelte';
import { results } from '$lib/searchResultState.svelte';

let { data }: PageProps = $props();

let pd = $state(undefined);

onMount(async () => {
  pd = await (await fetch(`http://localhost:5000/member?bioguideId=${data.bioguideId}`)).json();
  results.results = pd.bills.map(bill => bill.id);
});
</script>

<Header>
  <a href="/" class="-mt-1 mb-6 px-4 text-"><span class="font-bold">Bill</span>board</a>
  <h1 class="w-full max-w-[1000px] mx-auto my-8 text-2xl text-left font-bold text-white">
    {pd === undefined ? "Loading..." : `Bills Sponsored by ${pd.member.fullName}`}
  </h1>
</Header>

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
