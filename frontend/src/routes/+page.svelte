<script lang='ts'>
import { beforeNavigate, pushState } from '$app/navigation';
import { page } from '$app/state';
import Header from '$lib/header.svelte';
import SankeyPlot from '$lib/sankeyPlot.svelte';
import SearchResult from '$lib/searchResult.svelte';
import { results } from '$lib/searchResultState.svelte';

beforeNavigate(() => {
  pushState('', { searchText });
});

export const prerender = false;

let searchText = $state(page.state.searchText !== undefined ? page.state.searchText : '');

$inspect(searchText);

let results_promise = $derived.by(async () => {
  if (searchText === '') return [];
  const res = await fetch(
    `http://localhost:5000/search?q=${searchText}`,
  );
  let data: Array<any> = await res.json();
  results.results = data.map(result => result.id);
  return data;
});
</script>

<Header>
  <a href="/" class="my-16 px-4 text-6xl text-"><span class="font-bold">Bill</span>board</a>
  <p class="my-8 text-lg text-center text-white">Track pending and historical bills from the U.S. Congress</p>
  <div class="my-8">
    <input
      bind:value={searchText}
      class="w-[400px] h-full px-5 py-2.5 rounded-full text-xl bg-white text-black placeholder:text-gray-600"
      placeholder="Search for a bill to learn more about it"
      type="text"
    />
  </div>
</Header>

<div class="mt-8 mb-4 flex justify-center">
  <main class="w-full max-w-[1000px] mx-4">
    {#await results_promise}
      <div class="w-full text-center">
        <p class="text-gray-700">Loading...</p>
      </div>
      {:then results}
        {#if results.length > 0}
          <ul class="rounded-xl border border-gray-200 overflow-hidden divide-y divide-gray-200">
            {#each results as result}
              <SearchResult {result} {searchText} />
            {/each}
          </ul>
        {:else if searchText === ""}
          <section class="mt-8">
            <SankeyPlot/>
          </section>
        {:else}
          <div class="w-full text-center">
            <p class="text-gray-700">No results found</p>
          </div>
        {/if}
      {:catch error}
        <p class="m-4"><span class="text-red-500">Error:</span> {error.message}</p>
    {/await}
  </main>
</div>
