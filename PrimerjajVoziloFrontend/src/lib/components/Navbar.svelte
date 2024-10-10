<script>
  export let data;
</script>

<div class="navbar bg-blue-100 dark:bg-blue-700 dark:text-white">
  <div class="flex-1">
    <a href="/" class="btn btn-ghost text-xl">PrimerjajVozilo</a>
  </div>
  <div class="flex-none gap-2">
    <ul class="menu menu-horizontal px-1">
      <li><a>Avto.net API</a></li>
    </ul>
    {#if data.logged}
    <div class="dropdown dropdown-end">
      <!-- Profile avatar -->
      <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
        <div class="w-10 rounded-full">
          <img
              alt="Tailwind CSS Navbar component"
              src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
        </div>
      </div>
      <!-- Profile avatar dropdown -->
      <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
      <ul tabindex="0" class="menu menu-sm dropdown-content bg-blue-100 dark:bg-blue-700 rounded-box z-[1] mt-3 w-52 p-2 shadow">
        <li><a href="/uporabnik">Moje Primerjave</a></li>
        <li>
          <!-- svelte-ignore a11y-missing-attribute -->
          <a>Nastavitve</a>
        </li>
        <li><a href="/uporabnik/odjava">Odjava</a></li>
      </ul>
    </div>
    {:else}
    <ul class="menu menu-horizontal px-1">
      <li><a href="/prijava">Prijava</a></li>
    </ul>

    <a href="/registracija" class="menu menu-horizontal btn btn-outline dark:text-white px-1">
      Registriraj se
    </a>
    {/if}
  </div>
</div>