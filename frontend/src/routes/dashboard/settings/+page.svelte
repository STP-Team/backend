<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth.js';
	import { setBreadcrumbs } from '$lib/stores/breadcrumbs.js';
	import DashboardLayout from '$lib/components/dashboard-layout.svelte';

	let currentUser = $derived($authStore.user);

	onMount(() => {
		setBreadcrumbs([{ label: "Настройки" }]);
	});
</script>

<svelte:head>
	<title>Настройки - Adminer</title>
	<meta name="description" content="Настройки системы" />
</svelte:head>

<DashboardLayout title="Настройки">
	<p class="text-muted-foreground">
		Здесь будут размещены настройки системы.
	</p>
</DashboardLayout>