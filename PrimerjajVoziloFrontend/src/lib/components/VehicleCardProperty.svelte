<script>
    export let icon;
    export let description;
    export let value;
</script>

<div class="grid grid-rows-vehicle-info grid-cols-vehicle-info">
    <!-- Icon -->
    <div class="row-span-2 col-span-1 flex justify-center items-center">
        <svelte:component this={icon} class="text-4xl text-blue-800 dark:text-blue-400" />
    </div>
    <!-- Value description -->
    <div class="flex text-sm items-end text-stone-500">
        {description}
    </div>
    <!-- Actual value -->
    <div class="text-2xl flex items-start">
        {value}
    </div>
</div>