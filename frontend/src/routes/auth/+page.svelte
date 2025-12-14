<script lang="ts">
    import {Login} from 'sveltegram';
    import {onMount} from 'svelte';
    import {goto} from '$app/navigation';
    import {authActions, authStore} from '$lib/stores/auth.js';
    import {
        authenticateTelegram,
        getCurrentUser,
        getStoredToken,
        removeToken,
        storeToken,
        type TelegramAuthData
    } from '$lib/auth.js';
    import {Card, CardContent, CardDescription, CardHeader, CardTitle} from '$lib/components/ui';

    let mounted = false;
    let authError = '';
    let isLoading = false;

    // Get bot username from environment variables
    const botUsername = import.meta.env.VITE_TELEGRAM_BOT_USERNAME;

    onMount(async () => {
        mounted = true;

        // Check if already authenticated
        const token = getStoredToken();
        if (token) {
            await checkExistingAuth(token);
        }
    });

    async function checkExistingAuth(token: string) {
        authActions.setLoading(true);
        try {
            const user = await getCurrentUser(token);
            authActions.setAuthenticated(user, token);
            await goto('/dashboard');
        } catch (error) {
            // Token is invalid, remove it
            removeToken();
            authActions.logout();
            console.log('Token validation failed:', error);
        } finally {
            authActions.setLoading(false);
        }
    }

    async function handleTelegramAuth(authData: any) {
        authError = '';
        isLoading = true;
        authActions.setLoading(true);

        try {
            // Convert to the format expected by our backend
            const convertedAuthData: TelegramAuthData = {
                id: String(authData.id),
                first_name: authData.first_name,
                last_name: authData.last_name,
                username: authData.username,
                photo_url: authData.photo_url,
                auth_date: String(authData.auth_date),
                hash: authData.hash
            };

            // Authenticate with backend
            const tokenInfo = await authenticateTelegram(convertedAuthData);

            // Store token
            storeToken(tokenInfo.access_token);

            // Get user info
            const user = await getCurrentUser(tokenInfo.access_token);

            // Update auth store
            authActions.setAuthenticated(user, tokenInfo.access_token);

            // Redirect to dashboard
            await goto('/dashboard');
        } catch (error) {
            authError = error instanceof Error ? error.message : 'Ошибка авторизации';
            authActions.setError(authError);
        } finally {
            isLoading = false;
            authActions.setLoading(false);
        }
    }

    $: currentAuthState = $authStore;
</script>

<svelte:head>
    <title>Авторизация - Adminer</title>
    <meta name="description" content="Войдите в систему через Telegram"/>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-background p-4">
    <Card class="w-full max-w-md">
        <CardHeader class="text-center space-y-2">
            <div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-primary/10">
                <svg class="h-6 w-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
            </div>
            <CardTitle level={2}>Авторизация</CardTitle>
            <CardDescription>
                Используйте Telegram аккаунт, привязанный к <a href="https://t.me/stpsher_bot"
                                                               class="text-fg-brand hover:underline" target="_blank">@СТПшеру</a>
            </CardDescription>
        </CardHeader>
        <CardContent class="space-y-6">
            {#if currentAuthState.loading || isLoading}
                <div class="flex flex-col items-center space-y-4">
                    <div class="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent"></div>
                    <p class="text-sm text-muted-foreground">Авторизация...</p>
                </div>
            {:else if currentAuthState.isAuthenticated}
                <div class="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-md">
                    <p class="text-center text-sm">
                        Добро пожаловать, {currentAuthState.user?.fullname}!
                    </p>
                </div>
            {:else if mounted}
                <div class="flex flex-col items-center space-y-6">
                    <div class="telegram-widget-container">
                        <Login
                                username={botUsername}
                                onauth={handleTelegramAuth}
                                requestAccess={true}
                        />
                    </div>

                    {#if authError || currentAuthState.error}
                        <div class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-md w-full">
                            <p class="text-sm text-center">
                                {authError || currentAuthState.error}
                            </p>
                        </div>
                    {/if}

                    <div class="text-xs text-muted-foreground text-center">
                        <p>
                            Если войти не удается - напишите в <a href="https://t.me/stp_helpbot"
                                                                  class="text-fg-brand hover:underline" target="_blank">@ХелпБот</a>
                        </p>
                    </div>
                </div>
            {/if}
        </CardContent>
    </Card>
</div>

<style>
    .telegram-widget-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>