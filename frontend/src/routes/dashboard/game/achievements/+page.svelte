<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth.js';
	import { setBreadcrumbs } from '$lib/stores/breadcrumbs.js';
	import DashboardLayout from '$lib/components/dashboard-layout.svelte';

	let currentUser = $derived($authStore.user);

	onMount(() => {
		setBreadcrumbs([
			{ label: "Игра", href: "/dashboard/game" },
			{ label: "Достижения" }
		]);
	});
</script>

<svelte:head>
	<title>Достижения - Adminer</title>
	<meta name="description" content="Управление достижениями" />
</svelte:head>

<DashboardLayout title="Достижения">
	<p class="text-muted-foreground">
		Здесь будет размещен интерфейс управления достижениями.
	</p>
</DashboardLayout>