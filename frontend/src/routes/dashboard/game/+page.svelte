<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth.js';
	import { setBreadcrumbs } from '$lib/stores/breadcrumbs.js';
	import DashboardLayout from '$lib/components/dashboard-layout.svelte';

	let currentUser = $derived($authStore.user);

	onMount(() => {
		setBreadcrumbs([{ label: "Игра" }]);
	});
</script>

<svelte:head>
	<title>Игра - Adminer</title>
	<meta name="description" content="Управление игровой системой" />
</svelte:head>

<DashboardLayout title="Игра">
	<p class="text-muted-foreground">
		Здесь будет размещен интерфейс управления игровой системой.
	</p>
</DashboardLayout>