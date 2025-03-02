<script>
  import ExternalUrl from '$lib/externalUrl.svelte';

let { data } = $props();

const bill_promise = $derived.by(async () => {
    const res = await fetch(
        `http://localhost:5000/bill?id=${data.bill_id}`,
    );
    return await res.json();
});

function getStatus(bill) {
    if (bill == undefined) {
        return undefined;
    } else if (bill.actions[0]['actionCode'] == "36000" || bill.actions[0]['actionCode'] == "E40000") {
        return 'passed';
    } else if (bill.congress != "119") {
        return 'dead';
    } else {
        return 'pending';
    }
}
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
                <a class="font-regular px-2 py-1 text-xs rounded bg-white shadow" href="/sponsored-by/{sponsor.bioguideId}">
                    {sponsor.fullName}
                </a>
            {/each}
        {/await}
    </div>
</header>


<div class="mt-8 max-w-3xl mx-auto">
    <main class="shadow rounded-xl border border-gray-300 divide-y divide-gray-200">
        <div class="divide-x divide-gray-200 flex">
            <div class="p-4 flex-1">
                <h3 class="text-lg font-bold mb-2">Status</h3>
                <div class="flex justify-between items-center">
                    {#await bill_promise}
                        <div class="px-2 py-1 text-sm shadow bg-gray-200 flex gap-x-1 items-center rounded">
                            Loading 
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                            </svg>
                        </div>
                    {:then bill}
                        {#if getStatus(bill) == 'dead'}
                            <div class="px-2 py-1 text-sm shadow bg-red-200 flex gap-x-1 items-center rounded">
                                Dead 
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                            </div>
                        {:else if getStatus(bill) == 'passed'}
                            <div class="px-2 py-1 text-sm shadow bg-green-200 flex gap-x-1 items-center rounded">
                                Passed 
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                            </div>
                        {:else}
                            <div class="px-2 py-1 text-sm shadow bg-gray-200 flex gap-x-1 items-center rounded">
                                Pending 
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                            </div>
                        {/if}
                    {/await}
                    <div>
                        {#await bill_promise}
                            Loading...
                        {:then bill}
                            <ExternalUrl url={bill.url}>View on Congress.gov</ExternalUrl>
                        {/await}
                    </div>
                </div>
            </div>
            {#await bill_promise}
                <div class="p-4 flex-1 flex flex-col justify-between">
                    <h3 class="font-bold text-lg mb-2">Probability</h3>
                    <p>
                        Loading...
                    </p>
                </div>
            {:then bill}
                {#if getStatus(bill) == 'pending'}
                    <div class="p-4 flex-1 flex flex-col justify-between">
                        <h3 class="font-bold text-lg mb-2">Probability</h3>
                        <p>
                            This bill has a <span class="bg-yellow-100 px-1 py-0.5 rounded">{(bill.prediction.probability * 100).toFixed(0)}%</span> chance of being passed.
                        </p>
                    </div>
                {/if}
            {/await}
            
        </div>
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
