<script>
    // Components
    import AddVehicleBtn from "$lib/components/AddVehicleBtn.svelte";
    import VehicleCard from "$lib/components/VehicleCard.svelte";
    // API Client
    import { vehiclesStore, getVehicle } from "$lib/api/client.js";

    export let data;
    export let form;

    // Get query parameters. If any vehicles are in url, load them
    let showInput;
    if ($vehiclesStore.length === 0) {
        showInput = true;
    } else {
        showInput = false;
    }
</script>

<div class:justify-center={$vehiclesStore.length === 0} class="flex items-center gap-x-3 h-full px-4 bg-green-500 dark:bg-stone-600 overflow-x-auto">

    <div class="flex justify-start items-center gap-x-2 shrink-0">
        {#each $vehiclesStore as vehicle}
        <VehicleCard {vehicle} />
        {/each}
    </div>
    
    <AddVehicleBtn form={form} showInput={showInput} />
</div>
