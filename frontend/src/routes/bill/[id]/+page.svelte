<script lang="ts">
let { data } = $props();

let bill_promise = $derived.by(async () => {
    const res = await fetch(
        `http://localhost:5000/bill?id=${data.bill_id}`,
    );
    return await res.json();
});
</script>

<!-- <header>
    <h2>
        {#await bill_promise}
        Loading...
        {:then bill}
        {bill.title}
        {/await}
    </h2>
</header> -->

{#await bill_promise}
<p>Loading</p>
{:then bill}
    <h1>{bill.title}</h1>
    {@html bill.summary}
{/await}
