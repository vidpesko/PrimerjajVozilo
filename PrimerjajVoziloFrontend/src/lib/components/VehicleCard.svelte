<script>
    // Splide image slideshow
    import { Splide, SplideSlide } from '@splidejs/svelte-splide';
    // Images
    // Icons
    import SpeedometerIcon from "virtual:icons/ion/md-speedometer";
    import CalendarIcon from "virtual:icons/material-symbols/calendar-add-on-outline-rounded";
    import EngineIcon from "virtual:icons/mdi/engine-outline";
    import MoneyIcon from "virtual:icons/ri/money-euro-circle-line";
    import OptionsIcon from "virtual:icons/cil/options";
    import BrowserIcon from "virtual:icons/iconoir/open-in-browser";
    import HideIcon from "virtual:icons/material-symbols/arrow-drop-up-rounded";
    import ExpandIcon from "virtual:icons/material-symbols/arrow-drop-down-rounded";
    import InfoIcon from "virtual:icons/material-symbols/info-outline-rounded";
    import TrashIcon from "virtual:icons/material-symbols/delete-outline-sharp";
    // Components
    import VehicleCardProperty from './VehicleCardProperty.svelte';
    import { enhance } from '$app/forms';
    // .env values
    import { PUBLIC_GOOGLE_MAPS_API_KEY } from '$env/static/public';

    import { vehiclesStore } from '../api/client.js';

    export let vehicle;

    let collapsedVehicleDescEndIndex = 100;
    let descCollapsed = false;
    let needsCollapsing = false;
    if (vehicle.required.description.length > collapsedVehicleDescEndIndex) {
        needsCollapsing = true;
        descCollapsed = true;
    }

    // Generate Google Maps query link from retrieved location
    let location = vehicle.required.location;
    location = location.replaceAll(" ", "+");

    // Generate engine power in right format (kW will be displayed. if KM exists, they will be displayed as a tooltip)
    let power = vehicle.required.power;
    let fullPower;
    // If string has '(num KM)'
    if (power.match(/\(\d+\sKM\)/g)) {
        fullPower = power;
        power = power.replace(/\(\d+\sKM\)/g, "");
    }

    // Binding to delete card btn
    let deleteCardBtn;
</script>

<div class="w-[80vw] xl:w-[30vw] md:w-[40vw] h-[85vh] rounded-xl bg-white dark:bg-stone-800 shadow-sm overflow-x-hidden shrink-0 p-2 flex flex-col dark:text-white">
    <!-- Header -->
    <div class="flex justify-between items-center">
        <!-- Name -->
        <h3 class="my-2 font-bold">{vehicle.required.name}</h3>

        <!-- Options -->
        <div class="dropdown dropdown-end">
            <div tabindex="0" role="button" class=""><OptionsIcon /></div>
            <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
            <ul tabindex="0" class="dropdown-content menu bg-blue-100 dark:bg-blue-700 rounded-box z-[1] w-52 p-2 shadow-2xl">
                <li><a href="{vehicle.metadata.url}" class="flex items-center justify-between" target="_blank">Odpri v avto.net <BrowserIcon /></a></li>
                <li><button class="flex items-center justify-between text-red-600 dark:text-red-400" on:click={deleteCardBtn.click()}>Odstrani <TrashIcon /></button></li>
            </ul>
        </div>
    </div>

    <!-- Images -->
    <Splide options={{heightRatio: 0.6, gap: "1em", perPage: 1, perMove: 1}} aria-label="My Favorite Images">
        {#each vehicle.required.images as img}
        <SplideSlide class="flex justify-center">
            <img class="rounded-xl" src="{img}" alt="Car"/>
        </SplideSlide>
        {/each}
    </Splide>

    <!-- Data -->
    <div class="grow mt-4 flex flex-col h-auto">
        <!-- Important data / "required" -->
        <div class="grid md:grid-cols-2 md:grid-rows-2 grid-cols-1 grid-rows-4 mb-4">
            <!-- Mileage -->
            <VehicleCardProperty icon={SpeedometerIcon} description="Kilometri" value={(vehicle.required.mileage) ? vehicle.required.mileage + "km" : "/"} />
            <!-- First registration -->
            <VehicleCardProperty icon={CalendarIcon} description="1. registracija" value={(vehicle.required.firstRegistration) ? vehicle.required.firstRegistration.replaceAll("-", "/") : "/"} />
            <!-- Power -->
            {#if fullPower}
            <div class="tooltip tooltip-bottom tooltip-primary" data-tip={fullPower}>
                <VehicleCardProperty icon={EngineIcon} description="Moč" value={power} />
            </div>
            {:else}
            <VehicleCardProperty icon={EngineIcon} description="Moč" value={power} />
            {/if}
            <!-- Price -->
            <VehicleCardProperty icon={MoneyIcon} description="Cena" value={vehicle.required.price} />
        </div>

        <!-- Other data / "optional" -->
        <div class="border-t">
            {#each Object.entries(vehicle.other) as [key, value]}
            {#if value}
            <div class="flex justify-between border-b my-1">
                <p class="text-stone-400">{key}:</p>
                <p>{value}</p>
            </div>
            {/if}
            {/each}
        </div>

        <!-- Description -->
        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
        <div class="">
            <p class="text-stone-400">Opis:</p>
            <div class="">
                {#if descCollapsed}
                <p>{@html (vehicle.required.description === "None") ? "Ni opisa" : vehicle.required.description.slice(0, collapsedVehicleDescEndIndex)}...</p>
                {:else}
                <p>{@html (vehicle.required.description === "None") ? "Ni opisa" : vehicle.required.description.slice(0, -1)}</p>
                {/if}
            </div>
            {#if needsCollapsing}
            <button class="link link-info flex items-center" on:click={() => {
                // Show
                if (descCollapsed) {
                    descCollapsed = false;
                } else {
                    descCollapsed = true;
                }
            }}>
                {#if descCollapsed}
                Razkrij <ExpandIcon />
                {:else}
                Skrij <HideIcon />
                {/if}
            </button>
            {/if}
        </div>
    </div>

    <!-- Location -->
    <div class="my-2">
        <!-- svelte-ignore a11y-missing-attribute -->
        <iframe
            width="100%"
            height="200px"
            style="border:0"
            loading="lazy"
            allowfullscreen
            referrerpolicy="no-referrer-when-downgrade"
            src="https://www.google.com/maps/embed/v1/place?key={PUBLIC_GOOGLE_MAPS_API_KEY}
            &q={location}&zoom=9">
        </iframe>
    </div>

    <!-- Get in contact -->
    <button class="btn btn-info dark:text-white">Možnosti</button>

    <!-- Hidden form for deleting the card -->
    <form class="hidden" action="?/odstrani" use:enhance={() => {
                        return async ({ update, result }) => {
                            if (result.type !== "failure") {
                                vehiclesStore.removeVehicle(vehicle);
                            }
                            update();
                        }
                    }} method="post">
        <button bind:this={deleteCardBtn} class="">Odstrani</button>
    </form>
</div>