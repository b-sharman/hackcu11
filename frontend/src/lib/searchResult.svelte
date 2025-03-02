<script lang='ts'>
import { slide } from "svelte/transition";

let { result, searchText } = $props();

let expanded: boolean = $state(false);

async function expand() {
  // put fetch call here eventually for the summary
  expanded = !expanded;
}
</script>

<li>
  <button class="size-full text-left p-4 hover:bg-gray-200" onclick={expand}>

    <div class="flex flex-row gap-8">
      <div class="basis-full">
        <p class="text-lg font-bold">
          {@html result.title.replaceAll(new RegExp(searchText, 'gi'), `<span class="bg-yellow-200">${searchText}</span>`)}
          <!-- {@html result.title.replace(searchText, `<span class="bg-yellow-200">${searchText}</span>`)} -->
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
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
          tempor incididunt ut labore et dolore magnam aliquam quaerat
          voluptatem. Ut enim aeque doleamus animo, cum corpore dolemus, fieri
          tamen permagna accessio potest, si aliquod aeternum et infinitum
          impendere malum nobis opinemur. Quod idem licet transferre in
          voluptatem, ut postea variari voluptas distinguique possit, augeri
          amplificarique non possit. At etiam.
        </p>
        <div class="mt-2">
          <a class="text-sm text-blue-600 underline" target="_blank" href={result.url}>
            {result.url}
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline size-3 align-middle">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
            </svg>
          </a>
        </div>
      </div>
    {/if}

  </button>
</li>
