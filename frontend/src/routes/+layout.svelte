<script>
import '../app.css';

let { children } = $props();
</script>

<header class="h-16 flex flex-row overflow-hidden text-center">
  <h2 class="block size-full flex items-center justify-center">
    <a href="/" class="px-4 text-lg"><span class="font-bold">Bill</span>board</a>
  </h2>
</header>

{@render children()}
