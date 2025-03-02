<script>
import ExternalUrl from '$lib/externalUrl.svelte';
import Header from '$lib/header.svelte';
import { results } from '$lib/searchResultState.svelte.js';
import { Timeline, TimelineItem, TimelineSeparator, TimelineDot, TimelineConnector, TimelineContent } from 'svelte-vertical-timeline';

let { data } = $props();

let email = $state('');
let emailError = '';

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

async function subscribe() {
    if (!email.includes('@')) {
        emailError = 'Please enter a valid email address';
        return;
    }

    emailError = '';

    try {
        const res = await fetch(
            `http://localhost:5000/subscribe`,
            {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                method: 'POST',
                body: new URLSearchParams({
                    'email': email,
                    'bill_id': data.bill_id,
                }),
            }
        );

        if (!res.ok) {
            throw new Error('Subscription failed');
        }

        alert('You have successfully subscribed for this bill!');
    }
    catch (e) {
        console.error('Error:', e);
        alert('An error occurred while subscribing. Please try again later.');
    }
}
</script>

<Header>
    <a href="/" class="-mt-1 mb-6 px-4 text-"><span class="font-bold">Bill</span>board</a>
    <div class="w-full text-left">
        <h1 class="text-2xl text-white max-w-[1000px] mx-auto font-bold">
            {#await bill_promise}
                Loading...
            {:then bill}
                {bill.title}
            {/await}
        </h1>
        <div class="flex flex-row gap-x-2 mt-4 max-w-[1000px] mx-auto">
            {#await bill_promise}
                <p class="text-gray-200">Loading...</p>
            {:then bill}
                {#each bill.data.bill.sponsors as sponsor}
                    <a class="font-regular px-2 py-1 text-xs rounded bg-white text-gray-900 shadow" href="/sponsored-by/{sponsor.bioguideId}">
                        {sponsor.fullName}
                    </a>
                {/each}
            {/await}
        </div>
    </div>
</Header>


<div class="my-8 max-w-[1000px] mx-auto">
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
                            This bill has a <span class="bg-yellow-100 px-1 py-0.5 rounded">{bill.prediction.probability < 1 ? '<1' : (bill.prediction.probability * 100).toFixed(0)}%</span> chance of being passed.
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
            {#await bill_promise}
                Loading...
                {:then bill}
                <!-- To the best of my knowledge, the library doesn't allow removing the left side, but with a bit of Tailwind magic, we can infiltrate the component. -->
                <ul class="list-disc list-inside **:[&.opposite-block]:hidden">
                    <Timeline position="right">
                        {#each bill.actions.reverse() as action}
                            <TimelineItem>
                                <TimelineSeparator>
                                    <TimelineDot />
                                    <TimelineConnector />
                                </TimelineSeparator>
                                <TimelineContent>
                                    <p>{action.actionDate} — {action.text}</p>
                                </TimelineContent>
                            </TimelineItem>
                        {/each}
                    </Timeline>
                </ul>
            {/await}
        </div>
        {#await bill_promise}
        <div class="p-4">
            <h3 class="mb-2 text-lg font-bold">Related Bills</h3>
            <p class="mt-2">Loading...</p>
        </div>
        {:then bill}
            {#if bill.related.length}
                <div class="p-4">
                    <h3 class="mb-2 text-lg font-bold">Related Bills</h3>
                    <ul class="list-disc list-inside mt-2">
                        {#each bill.related as related}
                            <li><a class="text-blue-600 underline text-sm" href={related.url}>{related.title}</a></li>
                        {/each}
                    </ul>
                </div>
            {/if}
        {/await}
        <div class="p-4">
            <h3 class="mb-2 text-lg font-bold">Track Bill</h3>
            <ul class="space-y-2">
                <input type="email" bind:value={email} class="w-[300px] h-full px-5 py-2 rounded-full border border-1.5 border-gray-500 outline-accent-bg text-md" placeholder="Enter your email">
                <button onclick={subscribe} class="px-5 py-2 m-2 bg-purple-900 text-white rounded hover:cursor-pointer">Subscribe</button>
            </ul>
        </div>
    </main>
</div>
<div>
    {#if results.results[results.results.findIndex(id => id == +data.bill_id) - 1] != undefined }
        <div class="fixed left-0 top-0 bottom-0 flex flex-col justify-center p-4">
            <a href={`/bill/${results.results[results.results.findIndex(id => id == +data.bill_id) - 1]}`} aria-label="Previous bill">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
            </a>
        </div>
    {/if}
    {#if results.results[results.results.findIndex(id => id == +data.bill_id) + 1] != undefined }
        <div class="fixed right-0 top-0 bottom-0 flex flex-col justify-center p-4">
            <a href={`/bill/${results.results[results.results.findIndex(id => id == +data.bill_id) + 1]}`} aria-label="Next bill">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>
            </a>
        </div>
    {/if}
  </div>
