<script>
  // Main CSS
    import "../app.css";
    // Splide (image slideshow)
    import '@splidejs/svelte-splide/css';
    // Components
    import Navbar from "$lib/components/Navbar.svelte";

    export let data;
</script>

<div class="flex flex-col h-screen">
  <!-- Navbar -->
  <Navbar data={data} />
  
  <!-- Body -->
  <div class="grow">
    <slot />
  </div>
</div>