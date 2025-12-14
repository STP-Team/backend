<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth.js';
	import { setBreadcrumbs } from '$lib/stores/breadcrumbs.js';
	import DashboardLayout from '$lib/components/dashboard-layout.svelte';

	let currentUser = $derived($authStore.user);

	onMount(() => {
		setBreadcrumbs([
			{ label: "Игра", href: "/dashboard/game" },
			{ label: "Транзакции" }
		]);
	});
</script>

<svelte:head>
	<title>Транзакции - Adminer</title>
	<meta name="description" content="Управление игровыми транзакциями" />
</svelte:head>

<DashboardLayout title="Транзакции">
	<p class="text-muted-foreground">
		Здесь будет размещен интерфейс управления игровыми транзакциями.
	</p>
</DashboardLayout>