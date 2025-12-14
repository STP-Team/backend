<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth.js';
	import { setBreadcrumbs } from '$lib/stores/breadcrumbs.js';
	import DashboardLayout from '$lib/components/dashboard-layout.svelte';

	let currentUser = $derived($authStore.user);

	onMount(() => {
		setBreadcrumbs([{ label: "Сотрудники" }]);
	});
</script>

<svelte:head>
	<title>Сотрудники - Adminer</title>
	<meta name="description" content="Управление сотрудниками" />
</svelte:head>

<DashboardLayout title="Сотрудники">
	<p class="text-muted-foreground">
		Здесь будет размещен интерфейс управления сотрудниками.
	</p>
</DashboardLayout>