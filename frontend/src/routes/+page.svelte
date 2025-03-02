<script lang='ts'>
export const prerender = false;

let searchText = $state('');

let results_promise = $derived.by(async () => {
  const res = await fetch(
    `http://localhost:5000/search?q=${searchText}`,
  );
  return await res.json();
});

$inspect(searchText, results_promise);

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
    {#await results_promise}
      <p>Loading...</p>
      {:then results}
        {#if results.length > 0}
          {#each results as result}
            {console.log(result)}
            <p>{@html result.title.replace(searchText, `<strong>${searchText}</strong>`)}</p>
          {/each}
        {:else if searchText === ""}
          <p>Search results will appear here</p>
        {:else}
          <p>No results found</p>
        {/if}
      {:catch error}
        <p><span class="text-red-500">Error:</span> {error.message}</p>
    {/await}
  </div>

</main>
