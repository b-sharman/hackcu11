<script lang='ts'>
import SearchResult from '$lib/searchResult.svelte';

export const prerender = false;

let searchText = $state('');

let results_promise = $derived.by(async () => {
  if (searchText === '') return [];
  const res = await fetch(
    `http://localhost:5000/search?q=${searchText}`,
  );
  return await res.json();
});

</script>

<header class="bg-linear-to-br from-indigo-800 to-purple-900 py-6 px-2 flex flex-col items-center">
  <p class="my-12 text-lg text-center text-white">Track pending and historical bills from the U.S. Congress</p>
  <div class="my-8">
    <input
      bind:value={searchText}
      class="w-[400px] h-full px-5 py-2.5 rounded-full text-xl bg-white placeholder:text-gray-600"
      placeholder="Search for a bill to learn more about it"
      type="text"
    />
  </div>
</header>

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
</div>
