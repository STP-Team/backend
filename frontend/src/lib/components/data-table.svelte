<script lang="ts" generics="TData, TValue">
	import { type ColumnDef, getCoreRowModel, getSortedRowModel, getFilteredRowModel, type SortingState, type ColumnFiltersState } from "@tanstack/table-core";
	import { createSvelteTable, FlexRender } from "$lib/components/ui/data-table";
	import * as Table from "$lib/components/ui/table";

	type DataTableProps<TData, TValue> = {
		columns: ColumnDef<TData, TValue>[];
		data: TData[];
		globalFilterValue?: string;
		onSortingChange?: (sorting: SortingState) => void;
		onColumnFiltersChange?: (columnFilters: ColumnFiltersState) => void;
		sorting?: SortingState;
		columnFilters?: ColumnFiltersState;
	};

	let {
		data,
		columns,
		globalFilterValue = '',
		onSortingChange,
		onColumnFiltersChange,
		sorting = $bindable([]),
		columnFilters = $bindable([])
	}: DataTableProps<TData, TValue> = $props();

	const table = createSvelteTable({
		get data() {
			return data;
		},
		columns,
		state: {
			get sorting() {
				return sorting;
			},
			get columnFilters() {
				return columnFilters;
			},
			get globalFilter() {
				return globalFilterValue;
			}
		},
		onSortingChange: (updater) => {
			const newSorting = typeof updater === "function" ? updater(sorting) : updater;
			sorting = newSorting;
			onSortingChange?.(newSorting);
		},
		onColumnFiltersChange: (updater) => {
			const newColumnFilters = typeof updater === "function" ? updater(columnFilters) : updater;
			columnFilters = newColumnFilters;
			onColumnFiltersChange?.(newColumnFilters);
		},
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		getFilteredRowModel: getFilteredRowModel(),
	});
</script>

<div class="rounded-md border">
	<Table.Root>
		<Table.Header>
			{#each table.getHeaderGroups() as headerGroup}
				<Table.Row>
					{#each headerGroup.headers as header}
						<Table.Head>
							{#if !header.isPlaceholder}
								<FlexRender
									content={header.column.columnDef.header}
									context={header.getContext()}
								/>
							{/if}
						</Table.Head>
					{/each}
				</Table.Row>
			{/each}
		</Table.Header>
		<Table.Body>
			{#if table.getRowModel().rows?.length}
				{#each table.getRowModel().rows as row}
					<Table.Row>
						{#each row.getVisibleCells() as cell}
							<Table.Cell>
								<FlexRender
									content={cell.column.columnDef.cell}
									context={cell.getContext()}
								/>
							</Table.Cell>
						{/each}
					</Table.Row>
				{/each}
			{:else}
				<Table.Row>
					<Table.Cell colspan={columns.length} class="h-24 text-center">
						Нет данных
					</Table.Cell>
				</Table.Row>
			{/if}
		</Table.Body>
	</Table.Root>
</div>

<!-- Expose table instance for external access -->
{#snippet tableInstance()}
	{table}
{/snippet}