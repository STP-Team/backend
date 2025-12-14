<script lang="ts">
	import { goto } from '$app/navigation';
	import { authStore, authActions } from '$lib/stores/auth.js';
	import { removeToken } from '$lib/auth.js';

	function handleLogout() {
		removeToken();
		authActions.logout();
		goto('/auth');
	}

	$: currentUser = $authStore.user;
	$: isLoading = $authStore.loading;
</script>

<svelte:head>
	<title>Панель управления - Adminer</title>
	<meta name="description" content="Главная панель администратора" />
</svelte:head>

{#if isLoading}
	<div class="min-h-screen flex items-center justify-center">
		<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
	</div>
{:else if currentUser}
	<div class="min-h-screen bg-gray-50">
		<!-- Header -->
		<header class="bg-white shadow">
			<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<div class="flex justify-between items-center py-6">
					<div>
						<h1 class="text-3xl font-bold text-gray-900">Панель управления</h1>
						<p class="text-sm text-gray-600">Добро пожаловать, {currentUser.fullname}</p>
					</div>
					<div class="flex items-center space-x-4">
						<div class="text-sm text-gray-600">
							<p><strong>Роль:</strong> {currentUser.role === 3 ? 'Администратор' : `Роль ${currentUser.role}`}</p>
							{#if currentUser.username}
								<p><strong>Username:</strong> @{currentUser.username}</p>
							{/if}
							{#if currentUser.division}
								<p><strong>Отдел:</strong> {currentUser.division}</p>
							{/if}
							{#if currentUser.position}
								<p><strong>Должность:</strong> {currentUser.position}</p>
							{/if}
						</div>
						<button
							on:click={handleLogout}
							class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
						>
							Выйти
						</button>
					</div>
				</div>
			</div>
		</header>

		<!-- Main content -->
		<main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
			<div class="px-4 py-6 sm:px-0">
				<!-- Welcome Card -->
				<div class="bg-white overflow-hidden shadow rounded-lg mb-6">
					<div class="px-4 py-5 sm:p-6">
						<h2 class="text-lg font-medium text-gray-900 mb-4">
							Добро пожаловать в систему администрирования
						</h2>
						<p class="text-gray-600">
							Вы успешно авторизовались через Telegram. Теперь у вас есть доступ к панели управления.
						</p>
					</div>
				</div>

				<!-- User Info Card -->
				<div class="bg-white overflow-hidden shadow rounded-lg mb-6">
					<div class="px-4 py-5 sm:p-6">
						<h3 class="text-lg font-medium text-gray-900 mb-4">Информация о пользователе</h3>
						<dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
							<div>
								<dt class="text-sm font-medium text-gray-500">ID пользователя</dt>
								<dd class="mt-1 text-sm text-gray-900">{currentUser.user_id}</dd>
							</div>
							<div>
								<dt class="text-sm font-medium text-gray-500">Полное имя</dt>
								<dd class="mt-1 text-sm text-gray-900">{currentUser.fullname}</dd>
							</div>
							{#if currentUser.username}
								<div>
									<dt class="text-sm font-medium text-gray-500">Telegram username</dt>
									<dd class="mt-1 text-sm text-gray-900">@{currentUser.username}</dd>
								</div>
							{/if}
							<div>
								<dt class="text-sm font-medium text-gray-500">Уровень доступа</dt>
								<dd class="mt-1 text-sm text-gray-900">
									{#if currentUser.role === 3}
										<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
											Администратор
										</span>
									{:else}
										<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
											Роль {currentUser.role}
										</span>
									{/if}
								</dd>
							</div>
							{#if currentUser.division}
								<div>
									<dt class="text-sm font-medium text-gray-500">Отдел</dt>
									<dd class="mt-1 text-sm text-gray-900">{currentUser.division}</dd>
								</div>
							{/if}
							{#if currentUser.position}
								<div>
									<dt class="text-sm font-medium text-gray-500">Должность</dt>
									<dd class="mt-1 text-sm text-gray-900">{currentUser.position}</dd>
								</div>
							{/if}
						</dl>
					</div>
				</div>

				<!-- Quick Actions -->
				<div class="bg-white overflow-hidden shadow rounded-lg">
					<div class="px-4 py-5 sm:p-6">
						<h3 class="text-lg font-medium text-gray-900 mb-4">Быстрые действия</h3>
						<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
							<button class="relative bg-blue-50 p-6 rounded-lg hover:bg-blue-100 transition-colors">
								<div>
									<span class="inline-flex items-center justify-center p-3 bg-blue-600 rounded-md shadow-lg">
										<svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
										</svg>
									</span>
								</div>
								<div class="mt-4">
									<h3 class="text-lg font-medium text-gray-900">Пользователи</h3>
									<p class="mt-2 text-sm text-gray-500">
										Управление пользователями системы
									</p>
								</div>
							</button>

							<button class="relative bg-green-50 p-6 rounded-lg hover:bg-green-100 transition-colors">
								<div>
									<span class="inline-flex items-center justify-center p-3 bg-green-600 rounded-md shadow-lg">
										<svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
										</svg>
									</span>
								</div>
								<div class="mt-4">
									<h3 class="text-lg font-medium text-gray-900">Отчеты</h3>
									<p class="mt-2 text-sm text-gray-500">
										Просмотр и создание отчетов
									</p>
								</div>
							</button>

							<button class="relative bg-purple-50 p-6 rounded-lg hover:bg-purple-100 transition-colors">
								<div>
									<span class="inline-flex items-center justify-center p-3 bg-purple-600 rounded-md shadow-lg">
										<svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
										</svg>
									</span>
								</div>
								<div class="mt-4">
									<h3 class="text-lg font-medium text-gray-900">Настройки</h3>
									<p class="mt-2 text-sm text-gray-500">
										Конфигурация системы
									</p>
								</div>
							</button>
						</div>
					</div>
				</div>
			</div>
		</main>
	</div>
{/if}