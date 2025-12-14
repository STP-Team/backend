<script lang="ts">
    import {onMount} from 'svelte';
    import {goto} from '$app/navigation';
    import {authStore} from '$lib/stores/auth.js';
    import {getStoredToken} from '$lib/auth.js';

    onMount(async () => {
        await new Promise(resolve => setTimeout(resolve, 100));

        const authState = $authStore;
        if (authState.isAuthenticated && authState.user) {
            await goto('/dashboard');
            return;
        }

        const token = getStoredToken();
        if (token) {
            await goto('/dashboard');
        } else {
            await goto('/auth');
        }
    });
</script>

<svelte:head>
    <title>Adminer</title>
    <meta name="description" content="СТП Администрирование"/>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Загрузка...</p>
    </div>
</div>