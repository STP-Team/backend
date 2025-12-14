<script lang="ts">
    import './layout.css';
    import Footer from "./Footer.svelte";

    let {children} = $props();
</script>

<div class="app">
    <main>{@render children()}</main>
    <!-- <Footer/> -->
</div>

<style>
    .app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    main {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding: 1rem;
        width: 100%;
        margin: 0 auto;
        box-sizing: border-box;
    }
</style>
