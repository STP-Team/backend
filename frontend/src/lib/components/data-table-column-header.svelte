<script lang="ts">
	import { Button } from "$lib/components/ui/button";
	import type { Column } from "@tanstack/table-core";

	type Props = {
		column: Column<any, unknown>;
		title: string;
	};

	let { column, title }: Props = $props();
</script>

<Button
	variant="ghost"
	size="sm"
	class="-ml-3 h-8 data-[state=open]:bg-accent"
	onclick={column.getCanSort() ? column.getToggleSortingHandler() : undefined}
	disabled={!column.getCanSort()}
>
	<span>{title}</span>
	{#if column.getIsSorted() === "desc"}
		<span class="ml-2 text-xs">↓</span>
	{:else if column.getIsSorted() === "asc"}
		<span class="ml-2 text-xs">↑</span>
	{:else if column.getCanSort()}
		<span class="ml-2 text-xs opacity-50">↕</span>
	{/if}
</Button>