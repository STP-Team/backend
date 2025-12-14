<script lang="ts">
	import * as Avatar from "$lib/components/ui/avatar/index.js";
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import { useSidebar } from "$lib/components/ui/sidebar/index.js";
	import { goto } from '$app/navigation';
	import { authActions } from '$lib/stores/auth.js';
	import { removeToken } from '$lib/auth.js';
	import BadgeCheckIcon from "@lucide/svelte/icons/badge-check";
	import BellIcon from "@lucide/svelte/icons/bell";
	import ChevronsUpDownIcon from "@lucide/svelte/icons/chevrons-up-down";
	import CreditCardIcon from "@lucide/svelte/icons/credit-card";
	import LogOutIcon from "@lucide/svelte/icons/log-out";
	import SparklesIcon from "@lucide/svelte/icons/sparkles";
	import UserIcon from "@lucide/svelte/icons/user";

	let { user }: { user?: any } = $props();
	const sidebar = useSidebar();

	function handleLogout() {
		removeToken();
		authActions.logout();
		goto('/auth');
	}

	// Extract short name from fullname (first name and last name initials)
	function getShortName(fullname: string): string {
		if (!fullname) return "Пользователь";
		const parts = fullname.trim().split(' ').filter(Boolean);
		if (parts.length === 0) return "Пользователь";
		if (parts.length === 1) return parts[0];
		if (parts.length === 2) return `${parts[0]} ${parts[1][0]}.`;
		return `${parts[0]} ${parts[1][0]}.`;
	}

	// Generate initials from fullname
	function getInitials(fullname: string): string {
		if (!fullname) return "У";
		const parts = fullname.trim().split(' ').filter(Boolean);
		if (parts.length === 0) return "У";
		if (parts.length === 1) return parts[0][0]?.toUpperCase() || "У";
		return `${parts[0][0]?.toUpperCase() || ""}${parts[1][0]?.toUpperCase() || ""}`;
	}
</script>

<Sidebar.Menu>
	<Sidebar.MenuItem>
		<DropdownMenu.Root>
			<DropdownMenu.Trigger>
				{#snippet child({ props })}
					<Sidebar.MenuButton
						size="lg"
						class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
						{...props}
					>
						<Avatar.Root class="size-8 rounded-lg">
							<Avatar.Image src={user?.telegram_avatar || "/avatars/admin.jpg"} alt={user?.fullname || "Пользователь"} />
							<Avatar.Fallback class="rounded-lg">{user ? getInitials(user.fullname) : "У"}</Avatar.Fallback>
						</Avatar.Root>
						<div class="grid flex-1 text-start text-sm leading-tight">
							<span class="truncate font-medium">{user ? getShortName(user.fullname) : "Пользователь"}</span>
							<span class="truncate text-xs">{user?.role === 3 ? 'Администратор' : `Роль ${user?.role || 'неизвестна'}`}</span>
						</div>
						<ChevronsUpDownIcon class="ms-auto size-4" />
					</Sidebar.MenuButton>
				{/snippet}
			</DropdownMenu.Trigger>
			<DropdownMenu.Content
				class="w-(--bits-dropdown-menu-anchor-width) min-w-56 rounded-lg"
				side={sidebar.isMobile ? "bottom" : "right"}
				align="end"
				sideOffset={4}
			>
				<DropdownMenu.Label class="p-0 font-normal">
					<div class="flex items-center gap-2 px-1 py-1.5 text-start text-sm">
						<Avatar.Root class="size-8 rounded-lg">
							<Avatar.Image src={user?.telegram_avatar || "/avatars/admin.jpg"} alt={user?.fullname || "Пользователь"} />
							<Avatar.Fallback class="rounded-lg">{user ? getInitials(user.fullname) : "У"}</Avatar.Fallback>
						</Avatar.Root>
						<div class="grid flex-1 text-start text-sm leading-tight">
							<span class="truncate font-medium">{user?.fullname || "Пользователь"}</span>
							<span class="truncate text-xs">{user?.username ? `@${user.username}` : user?.role === 3 ? 'Администратор' : `Роль ${user?.role || 'неизвестна'}`}</span>
						</div>
					</div>
				</DropdownMenu.Label>
				<DropdownMenu.Separator />
				<DropdownMenu.Group>
					<DropdownMenu.Item>
						<UserIcon />
						Профиль
					</DropdownMenu.Item>
					<DropdownMenu.Item>
						<BellIcon />
						Уведомления
					</DropdownMenu.Item>
				</DropdownMenu.Group>
				<DropdownMenu.Separator />
				<DropdownMenu.Item onclick={handleLogout}>
					<LogOutIcon />
					Выйти
				</DropdownMenu.Item>
			</DropdownMenu.Content>
		</DropdownMenu.Root>
	</Sidebar.MenuItem>
</Sidebar.Menu>
