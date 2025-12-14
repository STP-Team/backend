<script lang="ts">
	import {onMount} from 'svelte';
	import {goto} from '$app/navigation';
	import {authActions, authStore} from '$lib/stores/auth.js';
	import {getCurrentUser, getStoredToken, removeToken} from '$lib/auth.js';
	import AppSidebar from '$lib/components/app-sidebar.svelte';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import Header from '../Header.svelte';

	let mounted = $state(false);

    onMount(async () => {
        mounted = true;

        // Only check auth if needed
        const currentState = $authStore;
        const isRecentlyValidated = currentState.lastValidated &&
            (Date.now() - currentState.lastValidated) < 5000; // 5 seconds

        if (!currentState.isAuthenticated || !currentState.user || !isRecentlyValidated) {
            await checkAuth();
        }
    });

    async function checkAuth() {
        const token = getStoredToken();

        if (!token) {
            await goto('/auth');
            return;
        }

        try {
            authActions.setLoading(true);
            const user = await getCurrentUser(token);
            authActions.setAuthenticated(user, token);
        } catch (error) {
            console.log('Dashboard auth check failed:', error);
            removeToken();
            authActions.logout();
            await goto('/auth');
        } finally {
            authActions.setLoading(false);
        }
    }

    let isAuthenticated = $derived($authStore.isAuthenticated);
    let isLoading = $derived($authStore.loading);
</script>

{#if isLoading}
    <div class="min-h-screen flex items-center justify-center bg-gray-50">
        <div class="text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-4 text-gray-600">Проверка авторизации...</p>
        </div>
    </div>
{:else if isAuthenticated && mounted}
    <Sidebar.Provider>
        <AppSidebar user={$authStore.user} />
        <Sidebar.Inset>
            <Header />
            <slot />
        </Sidebar.Inset>
    </Sidebar.Provider>
{/if}