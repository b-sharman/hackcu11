<script lang='ts'>
import { slide } from "svelte/transition";
  import ExternalUrl from "./externalUrl.svelte";

const READABLE_STRS = {
    'HCONRES': 'H.Con.Res.',
    'HJRES': 'H.J.Res.',
    'HR': 'H.R.',
    'HRES': 'H.Res.',
    'S': 'S.',
    'SCONRES': 'S.Con.Res.',
    'SJRES': 'S.J.Res.',
    'SRES': 'S.Res.',
}

let { result, searchText } = $props();

let expanded: boolean = $state(false);
let summary: string = $state('');

async function expand() {
  // put fetch call here eventually for the summary
  const json = await (await fetch(
    `http://localhost:5000/summary?id=${result.id}`,
  )).json();
  summary = json['exists'] ? json['summary'] : 'No summary is available for this bill.'
  expanded = !expanded;
}
</script>

<li class="hover:bg-gray-200">
  <button class="size-full text-left p-4" onclick={expand}>

    <div class="flex flex-row gap-8">
      <div class="basis-full">
        <p class="text-xs text-gray-600">{READABLE_STRS[result.type]}{result.number}</p>
        <p class="my-1 text-lg font-bold">
          {@html result.title.replaceAll(
            new RegExp(searchText, 'gi'),
            match => `<span class="bg-yellow-200">${match}</span>`
          )}
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
      <div class="mt-4" transition:slide>
        {@html summary}

        <div class="flex flex-row mt-2 gap-8">
          <div class="grow">
            <ExternalUrl url={result.url}>View on Congress.gov</ExternalUrl>
          </div>
          <div>
            <a class="mr-4 text-sm text-blue-600 underline" href="/bill/{result.id}">Learn more about this bill</a>
          </div>
        </div>
      </div>
    {/if}

  </button>
</li>
