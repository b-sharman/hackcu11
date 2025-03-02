<script>
let { children } = $props();
</script>

<header class="bg-linear-to-br from-indigo-800 to-fuchsia-900 py-6 px-2 flex flex-col items-center text-white">
  {@render children()}
</header>
