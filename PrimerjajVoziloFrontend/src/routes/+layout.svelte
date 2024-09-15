<script>
  // Main CSS
    import "../app.css";
    // Splide (image slideshow)
    import '@splidejs/svelte-splide/css';
    // Components
    import Navbar from "$lib/components/Navbar.svelte";
</script>

<div class="flex flex-col h-screen">
  <!-- Navbar -->
  <Navbar />
  
  <!-- Body -->
  <div class="grow">
    <slot />
  </div>
</div>