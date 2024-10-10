<script>
    // Svelte & SvelteKit
    import { enhance } from '$app/forms';
    import { page, navigating } from '$app/stores';
    // Icons
    import AddIcon from 'virtual:icons/bi/plus-lg';
    import CloseIcon from 'virtual:icons/bi/x-lg';
    // Components

    // API Client
    import { vehiclesStore } from '../api/client.js';

    export let showInput = false;
    export let form;

    let loading = false;
    let inputError = false;
</script>

<div class="flex items-center gap-2 p-2 shrink-0 rounded-xl bg-blue-50 dark:bg-blue-700" class:!bg-transparent={!showInput}>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="shrink-0 add-vehicle-btn-icon bg-stone-600 dark:bg-stone-400 hover:bg-blue-500" on:click={() => {showInput = !showInput}}>
        {#if showInput}
        <CloseIcon class="text-white" />
        {:else}
        <AddIcon class="text-white" />
        {/if}
    </div>

    {#if showInput}
    <div class="shrink-0">
        <form use:enhance={() => {
            // Start spinner
            loading = true;

            return async ({ update, result }) => {
                loading = false;
                // If url was invalid or any other error occurred on the server
                if (result.type !== "failure") {
                    vehiclesStore.addVehicle(result.data);
                } else {
                    inputError = true;
                }
                update();
            }
        }}
        action="?/dodaj"
        method="POST">
            {#if !loading}
            <!-- svelte-ignore a11y-autofocus -->
            <input autofocus name="url" type="text" placeholder="Prilepi avto.net povezavo" class="input w-full max-w-xs" class:input-error={inputError} />
            {:else}
            <span class="loading loading-dots loading-md"></span>
            {/if}

            {#if form?.error}
            <p class="text-red-600 mt-1">{form?.error}</p>
            {/if}
        </form>
    </div>
    {/if}
</div>