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

<div class="flex justify-center items-center gap-x-3 h-full bg-stone-100 overflow-x-scroll">
    {#each $vehiclesStore as vehicle}
    <VehicleCard {vehicle} />
    {/each}

    <AddVehicleBtn form={form} showInput={showInput} />
</div>
