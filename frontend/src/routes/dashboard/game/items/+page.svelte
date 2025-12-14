<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth.js';
	import { setBreadcrumbs } from '$lib/stores/breadcrumbs.js';
	import DashboardLayout from '$lib/components/dashboard-layout.svelte';

	let currentUser = $derived($authStore.user);

	onMount(() => {
		setBreadcrumbs([
			{ label: "Игра", href: "/dashboard/game" },
			{ label: "Предметы" }
		]);
	});
</script>

<svelte:head>
	<title>Предметы - Adminer</title>
	<meta name="description" content="Управление игровыми предметами" />
</svelte:head>

<DashboardLayout title="Предметы">
	<p class="text-muted-foreground">
		Здесь будет размещен интерфейс управления игровыми предметами.
	</p>
</DashboardLayout>