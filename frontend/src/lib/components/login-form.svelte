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
    import {FieldDescription,} from "$lib/components/ui/field/index.js";
    import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "$lib/components/ui/card/index.js";
    import * as HoverCard from "$lib/components/ui/hover-card";
    import * as Avatar from "$lib/components/ui/avatar";

    let mounted = $state(false);
    let authError = $state('');
    let isLoading = $state(false);

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

    let currentAuthState = $derived($authStore);
</script>

<Card class="mx-auto w-full max-w-sm">
    <CardHeader class="text-center space-y-2">
        <div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-primary/10">
            <svg class="h-6 w-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
        </div>
        <CardTitle class="text-2xl">Авторизация</CardTitle>
        <CardDescription>
            Используйте Telegram аккаунт, привязанный к
            <HoverCard.Root>
                <HoverCard.Trigger
                    href="https://t.me/stpsher_bot"
                    target="_blank"
                    rel="noreferrer noopener"
                    class="text-fg-brand rounded-sm underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-8 focus-visible:outline-black"
                >
                    @СТПшеру
                </HoverCard.Trigger>
                <HoverCard.Content class="w-80">
                    <div class="flex justify-between space-x-4">
                        <Avatar.Root>
                            <Avatar.Image src="https://t.me/i/userpic/320/stpsher_bot.jpg" alt="СТПшер бот"/>
                            <Avatar.Fallback>СТП</Avatar.Fallback>
                        </Avatar.Root>
                        <div class="space-y-1">
                            <h4 class="text-sm font-semibold">@СТПшер</h4>
                            <p class="text-sm">Графики, показатели, группы, игры</p>
                            <div class="flex items-center pt-2">
                                <svg class="me-2 size-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                </svg>
                                <span class="text-muted-foreground text-xs">
                                    Основной бот СТП
                                </span>
                            </div>
                        </div>
                    </div>
                </HoverCard.Content>
            </HoverCard.Root>
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

                <FieldDescription class="text-xs text-muted-foreground text-center">
                    Если войти не удается - напишите в <HoverCard.Root>
                <HoverCard.Trigger
                    href="https://t.me/stp_helpbot"
                    target="_blank"
                    rel="noreferrer noopener"
                    class="text-fg-brand rounded-sm underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-8 focus-visible:outline-black"
                >
                    @ХелпБот
                </HoverCard.Trigger>
                <HoverCard.Content class="w-80">
                    <div class="flex justify-between space-x-4">
                        <Avatar.Root>
                            <Avatar.Image src="https://t.me/i/userpic/320/stp_helpbot.jpg" alt="Хелп бот"/>
                            <Avatar.Fallback>ХелпБот</Avatar.Fallback>
                        </Avatar.Root>
                        <div class="space-y-1">
                            <h4 class="text-sm font-semibold">@ХелпБот</h4>
                            <p class="text-sm">Бот для помощи в решении технических сложностей</p>
                            <div class="flex items-center pt-2">
                                <svg class="me-2 size-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                </svg>
                                <span class="text-muted-foreground text-xs">
                                    Вспомогательный бот СТП
                                </span>
                            </div>
                        </div>
                    </div>
                </HoverCard.Content>
            </HoverCard.Root>
                </FieldDescription>
            </div>
        {/if}
    </CardContent>
</Card>

<style>
    .telegram-widget-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
