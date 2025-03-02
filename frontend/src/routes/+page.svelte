<script lang='ts'>
import SearchResult from '$lib/searchResult.svelte';
import { results } from '$lib/searchResultState.svelte';
export const prerender = false;

let searchText = $state('');

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

<header class="p-8 bg-purple-200 *:text-center">
  <h1 class="text-2xl m-4"><span class="font-bold">Bill</span>board</h1>
  <p class="text-gray-600">Track pending and historical bills from the U.S. Congress</p>
</header>

<main class="max-w-[1000px] mx-auto px-4 pb-4">
  <div class="my-16 flex justify-center gap-4">
    <input
      bind:value={searchText}
      class="w-[400px] h-full px-5 py-2.5 rounded-full border border-2 border-gray-500 outline-accent-bg text-lg"
      placeholder="Search for a bill to learn more about it"
      type="text"
    />
  </div>

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
        <div class="w-full text-center">
          <p class="text-gray-700">Search results will appear here</p>
        </div>
      {:else}
        <div class="w-full text-center">
          <p class="text-gray-700">No results found</p>
        </div>
      {/if}
    {:catch error}
      <p class="m-4"><span class="text-red-500">Error:</span> {error.message}</p>
  {/await}
</main>


