<script>
    export let form;
</script>

<div class=" h-full flex justify-center items-center">
    <div class="w-2/6 h-1/4 bg-blue-700 flex flex-col justify-center gap-y-4 rounded p-4">
        <h1 class="text-2xl text-white">Prijavi se:</h1>

        <form action="?/prijavi" method="post" class="flex flex-col gap-y-4 items-center">
            <!-- Username/email -->
            <label class="input input-bordered flex items-center gap-2 w-full" class:input-error={form?.error}>
                Ime:
                <input type="text" name="email" class="grow" placeholder="" />
            </label>

            <!-- Geslo -->
            <label class="input input-bordered flex items-center gap-2 w-full" class:input-error={form?.error}>
                Geslo:
                <input type="password" name="password" class="grow" placeholder="" />
            </label>

            {#if form?.error}
            {#each Object.values(form.error) as error}
            <p class="text-red-500">
                {error}
            </p>
            {/each}
            {/if}


            <button class="btn bg-white hover:text-white border-white text-black w-2/6">Prijavi se</button>
        </form>
    </div>
</div>