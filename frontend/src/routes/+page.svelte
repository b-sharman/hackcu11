<script lang='ts'>
import type { PageProps } from './$types';
import Fuse from 'fuse.js';

let { data }: PageProps = $props();

const fuse = new Fuse(data.titles, {});

let searchText = $state('');

let results = $derived(fuse.search(searchText));

</script>

<header class="p-8 bg-purple-200 *:text-center">
  <h1 class="text-2xl m-4 font-bold">App Name</h1>
  <p class="text-gray-600">Visualize public data from the U.S. Congress</p>
</header>

<main class="max-w-[1000px] mx-auto">
  <div class="my-16 flex justify-center gap-4">
    <input
      bind:value={searchText}
      class="h-full px-4 py-1.5 rounded border border-black h-[30px]"
      placeholder="Search for a bill to learn more about it"
      type="text"
    />
    <button class="h-full bg-accent-bg text-accent-fg px-4 py-1.5 rounded cursor-pointer">Search</button>
  </div>

  <div>
    {#if results.length > 0}
      {#each results.slice(0, 5) as result}
        <p>{result.item}</p>
      {/each}
    {:else if searchText === ""}
      <p>Search results will appear here</p>
    {:else}
      <p>No results found</p>
    {/if}
  </div>

</main>
