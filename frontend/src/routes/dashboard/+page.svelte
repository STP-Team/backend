<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/auth.js';
	import { setBreadcrumbs } from '$lib/stores/breadcrumbs.js';
	import DashboardLayout from '$lib/components/dashboard-layout.svelte';

	let currentUser = $derived($authStore.user);

	onMount(() => {
		setBreadcrumbs([{ label: "Главная" }]);
	});
</script>

<svelte:head>
	<title>Панель управления - Adminer</title>
	<meta name="description" content="Главная панель администратора" />
</svelte:head>

<DashboardLayout title="Добро пожаловать, {currentUser?.fullname || 'Пользователь'}">
	{#snippet children()}
		<p class="text-muted-foreground">
			Вы успешно авторизовались через Telegram. Используйте боковую панель для навигации по системе.
		</p>
	{/snippet}
</DashboardLayout>
