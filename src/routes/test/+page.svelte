<script lang='ts'>
import type { PageProps } from './$types';

let { data }: PageProps = $props();

</script>

<main class="max-w-[1000px] mx-auto">
  <h1 class="text-4xl font-bold my-6">Recent Bills</h1>

  {#each data.bills as bill}
    <div class="my-4 p-4 rounded border border-gray-400">
      <h2 class="text-lg mb-4">{bill.title}</h2>
      <p>Summary text here...</p>
    </div>
  {/each}

</main>
