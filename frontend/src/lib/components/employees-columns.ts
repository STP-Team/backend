import type { ColumnDef } from "@tanstack/table-core";
import { renderComponent } from "$lib/components/ui/data-table";
import DataTableColumnHeader from "$lib/components/data-table-column-header.svelte";
import type { Employee } from "$lib/api/employees.js";

// Role mapping with names and emojis
const ROLES = {
	0: { name: "Не авторизован", emoji: "" },
	1: { name: "Специалист", emoji: "👤" },
	2: { name: "Руководитель", emoji: "👑" },
	3: { name: "Дежурный", emoji: "👮‍♂️" },
	4: { name: "Администратор", emoji: "🛡️" },
	5: { name: "ГОК", emoji: "🔎" },
	6: { name: "МИП", emoji: "📝" },
	7: { name: "Рекрутер", emoji: "🙋🏻‍♂️" },
	10: { name: "root", emoji: "⚡" }
} as const;

function getRoleName(roleId: number): string {
	return ROLES[roleId as keyof typeof ROLES]?.name || `Роль ${roleId}`;
}

function getRoleEmoji(roleId: number): string {
	return ROLES[roleId as keyof typeof ROLES]?.emoji || '';
}

export const columns: ColumnDef<Employee>[] = [
	{
		accessorKey: "fullname",
		header: ({ column }) => renderComponent(DataTableColumnHeader, {
			column,
			title: "ФИО"
		}),
		cell: ({ getValue }) => {
			const value = getValue() as string;
			return `<span class="font-medium">${value}</span>`;
		}
	},
	{
		accessorKey: "position",
		header: ({ column }) => renderComponent(DataTableColumnHeader, {
			column,
			title: "Должность"
		}),
		cell: ({ getValue }) => {
			const value = getValue() as string | null;
			return `<span class="text-muted-foreground">${value || '—'}</span>`;
		}
	},
	{
		accessorKey: "division",
		header: ({ column }) => renderComponent(DataTableColumnHeader, {
			column,
			title: "Подразделение"
		}),
		cell: ({ getValue }) => {
			const value = getValue() as string | null;
			return `<span class="text-muted-foreground">${value || '—'}</span>`;
		}
	},
	{
		accessorKey: "head",
		header: ({ column }) => renderComponent(DataTableColumnHeader, {
			column,
			title: "Руководитель"
		}),
		cell: ({ getValue }) => {
			const value = getValue() as string | null;
			return `<span class="text-muted-foreground">${value || '—'}</span>`;
		}
	},
	{
		accessorKey: "email",
		header: ({ column }) => renderComponent(DataTableColumnHeader, {
			column,
			title: "Email"
		}),
		cell: ({ getValue }) => {
			const value = getValue() as string | null;
			return `<span class="text-muted-foreground">${value || '—'}</span>`;
		}
	},
	{
		accessorKey: "username",
		header: "Telegram",
		cell: ({ getValue }) => {
			const value = getValue() as string | null;
			return `<span class="text-muted-foreground">${value ? `@${value}` : '—'}</span>`;
		}
	},
	{
		accessorKey: "role",
		header: ({ column }) => renderComponent(DataTableColumnHeader, {
			column,
			title: "Роль"
		}),
		cell: ({ getValue }) => {
			const role = getValue() as number;
			const emoji = getRoleEmoji(role);
			const name = getRoleName(role);
			return `<span class="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800">${emoji} ${name}</span>`;
		}
	},
	{
		id: "status",
		header: "Статус",
		cell: ({ row }) => {
			const employee = row.original;
			let badges = '<div class="flex gap-1 flex-wrap">';

			if (employee.is_trainee) {
				badges += '<span class="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800">Стажер</span>';
			}
			if (employee.is_casino_allowed) {
				badges += '<span class="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-green-100 text-green-800">Казино</span>';
			}
			if (employee.is_exchange_banned) {
				badges += '<span class="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-red-100 text-red-800">Обмен запрещен</span>';
			}

			badges += '</div>';
			return badges;
		}
	}
];