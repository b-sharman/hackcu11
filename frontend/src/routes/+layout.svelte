<script>
import '../app.css';

let { children } = $props();
</script>

<div class="max-w-[1000px] mx-auto mt-8 mb-12">
  <header class="h-12 border border-2 border-purple-900 rounded-full flex flex-row overflow-hidden text-center">
    <button
      aria-label="back"
      class="block aspect-square rounded-full hover:bg-gray-200 flex justify-center items-center"
      onclick={() => {history.back();}}
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-4">
        <path fill-rule="evenodd" d="M7.72 12.53a.75.75 0 0 1 0-1.06l7.5-7.5a.75.75 0 1 1 1.06 1.06L9.31 12l6.97 6.97a.75.75 0 1 1-1.06 1.06l-7.5-7.5Z" clip-rule="evenodd" />
      </svg>
    </button>
    <h2 class="block size-full flex items-center justify-center">
      <a href="/" class="px-4 text-lg"><span class="font-bold">Bill</span>board</a>
    </h2>
    <div class="aspect-square"></div>
  </header>
</div>

{@render children()}
