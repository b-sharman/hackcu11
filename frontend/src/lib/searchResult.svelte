<script lang='ts'>
import { slide } from "svelte/transition";

let { result, searchText } = $props();

let expanded: boolean = $state(false);
let summary: string = $state('');

async function expand() {
  // put fetch call here eventually for the summary
  const json = await (await fetch(
    `http://localhost:5000/summary?id=${result.id}`,
  )).json();
  if (json['exists']) {
    // Remove the title if it's included in the summary
    summary = json['summary'].replace(`<b>${result.title}</b>`, '');
  } else {
    summary = 'No summary is available for this bill.';
  }
  expanded = !expanded;
}
</script>

<li>
  <button class="size-full text-left p-4 hover:bg-gray-200" onclick={expand}>

    <div class="flex flex-row gap-8">
      <div class="basis-full">
        <p class="text-lg font-bold">
          {@html result.title.replaceAll(
            new RegExp(searchText, 'gi'),
            match => `<span class="bg-yellow-200">${match}</span>`)
          }
        </p>
        <p class="text-sm text-gray-600">{new Intl.DateTimeFormat().format(new Date(result.date_introduced))}</p>
      </div>
      <div class="h-full">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6 transition {expanded ? 'rotate-90' : ''}">
          <path fill-rule="evenodd" d="M16.28 11.47a.75.75 0 0 1 0 1.06l-7.5 7.5a.75.75 0 0 1-1.06-1.06L14.69 12 7.72 5.03a.75.75 0 0 1 1.06-1.06l7.5 7.5Z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>

    {#if expanded}
      <div class="mt-4" in:slide out:slide>
        {@html summary}

        <div class="flex flex-row mt-2 gap-8">
          <div class="grow">
            <a class="text-sm text-blue-600 underline" target="_blank" href={result.url}>
              {result.url}
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline size-3 align-middle">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
              </svg>
            </a>
          </div>
          <div>
            <a class="mr-4 text-sm text-blue-600 underline" href="/bill/{result.id}">Learn more about this bill</a>
          </div>
        </div>
      </div>
    {/if}

  </button>
</li>
