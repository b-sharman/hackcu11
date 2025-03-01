<script lang='ts'>
import type { PageProps } from './$types';
import Fuse from 'fuse.js';

let { data }: PageProps = $props();

const fuse = new Fuse(
  data.members,
  {
    keys: ['name'],
  }
);

let searchText = $state('');

let results = $derived(fuse.search(searchText));

</script>

<main class="max-w-[1000px] mx-auto">
  <input type="search" placeholder="Search Congress members..." bind:value={searchText} />
  {#each results.slice(0, 5) as result}
    <p>{result.item.name}</p>
  {/each}

</main>
