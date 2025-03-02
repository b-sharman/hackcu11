<script lang="ts">
let { data } = $props();

let bill_promise = $derived.by(async () => {
    const res = await fetch(
        `http://localhost:5000/bill?id=${data.bill_id}`,
    );
    return await res.json();
});
</script>

<header class="font-bold bg-purple-200 py-6 px-2 flex justify-center">
    <span></span>
    <h2 class="text-2xl max-w-3xl">
        {#await bill_promise}
        Loading...
        {:then bill}
        {bill.title}
        {/await}
    </h2>
</header>
<main>
    {#await bill_promise}
        Loading...
    {:then bill}
        {@html bill.summary}
    {/await}
</main>
