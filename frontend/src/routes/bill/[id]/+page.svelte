<script lang="ts">
    let { data } = $props();
    let bill_promise = $derived.by(async () => {
        const res = await fetch(
            `http://localhost:5000/bill?id=${data.bill_id}`,
        );
        return await res.json();
    });
</script>

<div>
    {#await bill_promise}
    <p>Loading</p>
    {:then bill}
        <h1>{bill.title}</h1>
    {/await}
</div>
