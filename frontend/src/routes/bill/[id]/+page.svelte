<script lang="ts">
let { data } = $props();

let bill_promise = $derived.by(async () => {
    const res = await fetch(
        `http://localhost:5000/bill?id=${data.bill_id}`,
    );
    return await res.json();
});
</script>


<header class="bg-purple-200 py-6 px-2">
    <h2 class="text-2xl max-w-3xl mx-auto font-bold">
        {#await bill_promise}
        Loading...
        {:then bill}
        {bill.title}
        {/await}
    </h2>
    <div class="flex flex-row gap-x-2 mt-4 max-w-3xl mx-auto">
        {#await bill_promise}
            Loading...
        {:then bill}
            {#each bill.data.bill.sponsors as sponsor}
                <span class="font-regular px-2 py-1 text-xs rounded bg-white shadow">{sponsor.fullName}</span>
            {/each}
        {/await}
    </div>
</header>

<div class="mt-8 max-w-3xl mx-auto">
    <main class="shadow rounded-xl border border-gray-300 divide-y divide-gray-200">
        {#await bill_promise}
            <div class="p-4">
                <h3 class="mb-2 text-lg font-bold">Summary</h3>
                <div class="space-y-2">
                    Loading
                </div>
            </div>
        {:then bill}
            {#if bill.summary.exists}
                <div class="p-4">
                    <h3 class="mb-2 text-lg font-bold">Summary</h3>
                    <div class="space-y-2">
                        {@html bill.summary.summary}
                    </div>
                </div>
            {/if}
        {/await}
        <div class="p-4">
            <h3 class="mb-2 text-lg font-bold">Actions</h3>
            <ul class="list-disc list-inside">
                {#await bill_promise}
                    Loading...
                {:then bill}
                    {#each bill.actions as action}
                        <li>{action.actionDate} — {action.text}</li>
                    {/each}
                {/await}
            </ul>
        </div>
    </main>
</div>
