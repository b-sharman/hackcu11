<script lang='ts'>
  let { result, searchText } = $props();
</script>

<li class="block p-4 hover:bg-gray-200">
  <div class="flex flex-row gap-8">
    <p class="basis-full text-lg font-bold">
      {@html result.title.replaceAll(new RegExp(searchText, 'gi'), `<span class="bg-yellow-200">${searchText}</span>`)}
      <!-- {@html result.title.replace(searchText, `<span class="bg-yellow-200">${searchText}</span>`)} -->
    </p>
    <p class="text-sm text-gray-600">{new Intl.DateTimeFormat().format(new Date(result.date_introduced))}</p>
  </div>
  <a class="text-sm text-blue-600 underline" target="_blank" href={result.url}>
    {result.url}
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline size-3 align-middle">
      <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
    </svg>
  </a>
</li>
