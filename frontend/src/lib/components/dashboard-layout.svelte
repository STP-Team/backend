<script lang="ts">
	let {
		title = "Страница",
		children
	}: {
		title?: string;
		children?: import('svelte').Snippet;
	} = $props();
</script>

<div class="flex flex-1 flex-col gap-4 p-4">
	<div class="min-h-96 flex-1 rounded-xl bg-muted/50 md:min-h-min">
		<div class="p-6">
			<h1 class="mb-4 text-2xl font-bold">{title}</h1>
			{#if children}
				{@render children()}
			{/if}
		</div>
	</div>
</div>