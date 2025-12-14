<script lang="ts" module>
	import BuildingIcon from "@lucide/svelte/icons/building";
	import ChartPieIcon from "@lucide/svelte/icons/chart-pie";
	import HomeIcon from "@lucide/svelte/icons/home";
	import Settings2Icon from "@lucide/svelte/icons/settings-2";
	import ShieldCheckIcon from "@lucide/svelte/icons/shield-check";
	import UsersIcon from "@lucide/svelte/icons/users";
	import DatabaseIcon from "@lucide/svelte/icons/database";
	import MonitorIcon from "@lucide/svelte/icons/monitor";

	const staticData = {
		teams: [
			{
				name: "Дом.ру",
				logo: BuildingIcon,
				plan: "Корпоративный",
			},
		],
		navMain: [
			{
				title: "Главная",
				url: "/dashboard",
				icon: HomeIcon,
				isActive: true,
			},
			{
				title: "Сотрудники",
				url: "/dashboard/employees",
				icon: UsersIcon,
				items: [
					{
						title: "Список сотрудников",
						url: "/dashboard/employees",
					},
					{
						title: "Роли и права",
						url: "/dashboard/employees/roles",
					},
					{
						title: "Активные сессии",
						url: "/dashboard/employees/sessions",
					},
				],
			},
			{
				title: "Отчеты",
				url: "/dashboard/reports",
				icon: ChartPieIcon,
				items: [
					{
						title: "Аналитика",
						url: "/dashboard/reports/analytics",
					},
					{
						title: "Статистика",
						url: "/dashboard/reports/statistics",
					},
					{
						title: "Экспорт данных",
						url: "/dashboard/reports/export",
					},
				],
			},
			{
				title: "Настройки",
				url: "/dashboard/settings",
				icon: Settings2Icon,
				items: [
					{
						title: "Общие",
						url: "/dashboard/settings/general",
					},
					{
						title: "Безопасность",
						url: "/dashboard/settings/security",
					},
					{
						title: "Интеграции",
						url: "/dashboard/settings/integrations",
					},
					{
						title: "Резервное копирование",
						url: "/dashboard/settings/backup",
					},
				],
			},
		],
		projects: [
			{
				name: "Система мониторинга",
				url: "/dashboard/monitoring",
				icon: MonitorIcon,
			},
			{
				name: "База данных",
				url: "/dashboard/database",
				icon: DatabaseIcon,
			},
			{
				name: "Аудит безопасности",
				url: "/dashboard/security-audit",
				icon: ShieldCheckIcon,
			},
		],
	};
</script>

<script lang="ts">
	import NavMain from "./nav-main.svelte";
	import NavProjects from "./nav-projects.svelte";
	import NavUser from "./nav-user.svelte";
	import TeamSwitcher from "./team-switcher.svelte";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import type { ComponentProps } from "svelte";

	let {
		user,
		ref = $bindable(null),
		collapsible = "icon",
		...restProps
	}: ComponentProps<typeof Sidebar.Root> & { user?: any } = $props();
</script>

<Sidebar.Root {collapsible} {...restProps}>
	<Sidebar.Header>
		<TeamSwitcher teams={staticData.teams} />
	</Sidebar.Header>
	<Sidebar.Content>
		<NavMain items={staticData.navMain} />
		<NavProjects projects={staticData.projects} />
	</Sidebar.Content>
	<Sidebar.Footer>
		<NavUser {user} />
	</Sidebar.Footer>
	<Sidebar.Rail />
</Sidebar.Root>
