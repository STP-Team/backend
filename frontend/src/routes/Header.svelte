<script lang="ts">
    import { onMount } from 'svelte';
    import { ModeWatcher, toggleMode } from "mode-watcher";
    import { Button } from '$lib/components/ui/button/index.js';
    import * as Sidebar from '$lib/components/ui/sidebar/index.js';
    import { checkApiHealth, type HealthStatus } from '$lib/api/health.js';
    import { breadcrumbsStore } from '$lib/stores/breadcrumbs.js';
    import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
    import { Separator } from '$lib/components/ui/separator/index.js';
    import SunIcon from '@lucide/svelte/icons/sun';
    import MoonIcon from '@lucide/svelte/icons/moon';
    import WifiIcon from '@lucide/svelte/icons/wifi';
    import WifiOffIcon from '@lucide/svelte/icons/wifi-off';
    import AlertTriangleIcon from '@lucide/svelte/icons/alert-triangle';

    // API Health status
    let healthStatus = $state<HealthStatus>({ status: 'unknown', timestamp: 0 });
    let healthCheckInterval: number;

    async function updateHealthStatus() {
        healthStatus = await checkApiHealth();
    }

    function getHealthStatusColor() {
        switch (healthStatus.status) {
            case 'healthy':
                return 'text-green-600';
            case 'unhealthy':
                return 'text-red-600';
            default:
                return 'text-yellow-600';
        }
    }

    function getHealthStatusText() {
        switch (healthStatus.status) {
            case 'healthy':
                return 'API в норме';
            case 'unhealthy':
                return `API недоступен${healthStatus.details ? ': ' + healthStatus.details : ''}`;
            default:
                return 'Проверка API...';
        }
    }

    onMount(() => {
        // Initial health check
        updateHealthStatus();

        // Check health every 30 seconds
        healthCheckInterval = setInterval(updateHealthStatus, 30000) as unknown as number;

        return () => {
            if (healthCheckInterval) {
                clearInterval(healthCheckInterval);
            }
        };
    });
</script>

<ModeWatcher/>

<header class="flex h-16 items-center justify-between border-b bg-background px-4">
    <!-- Left side: Sidebar toggle and breadcrumbs -->
    <div class="flex items-center gap-2 flex-1">
        <Sidebar.Trigger />

        <Separator orientation="vertical" class="me-2 data-[orientation=vertical]:h-4" />

        <Breadcrumb.Root>
            <Breadcrumb.List>
                <Breadcrumb.Item class="hidden md:block">
                    <Breadcrumb.Link href="/dashboard">Панель управления</Breadcrumb.Link>
                </Breadcrumb.Item>
                {#each $breadcrumbsStore as breadcrumb (breadcrumb.label)}
                    <Breadcrumb.Separator class="hidden md:block" />
                    <Breadcrumb.Item>
                        {#if breadcrumb.href}
                            <Breadcrumb.Link href={breadcrumb.href}>{breadcrumb.label}</Breadcrumb.Link>
                        {:else}
                            <Breadcrumb.Page>{breadcrumb.label}</Breadcrumb.Page>
                        {/if}
                    </Breadcrumb.Item>
                {/each}
            </Breadcrumb.List>
        </Breadcrumb.Root>
    </div>

    <!-- Right side: API status and theme toggle -->
    <div class="flex items-center gap-2">
        <!-- API Health Status -->
        <div class="flex items-center gap-2 px-2 py-1 rounded-md border">
            {#snippet statusIcon()}
                {#if healthStatus.status === 'healthy'}
                    <WifiIcon class="h-4 w-4 {getHealthStatusColor()}" />
                {:else if healthStatus.status === 'unhealthy'}
                    <WifiOffIcon class="h-4 w-4 {getHealthStatusColor()}" />
                {:else}
                    <AlertTriangleIcon class="h-4 w-4 {getHealthStatusColor()}" />
                {/if}
            {/snippet}

            {@render statusIcon()}
            <span class="text-xs {getHealthStatusColor()}" title={getHealthStatusText()}>
                {healthStatus.status === 'healthy' ? 'API' : 'API недоступен'}
            </span>
        </div>

        <!-- Theme Toggle -->
        <Button onclick={toggleMode} variant="outline" size="icon">
            <SunIcon
                class="h-[1.2rem] w-[1.2rem] scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90"
            />
            <MoonIcon
                class="absolute h-[1.2rem] w-[1.2rem] scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0"
            />
            <span class="sr-only">Изменить тему</span>
        </Button>
    </div>
</header>
