<script lang="ts">
	import { cn } from "$lib/utils";
	import type { HTMLAttributes } from "svelte/elements";

	type $$Props = HTMLAttributes<HTMLHeadingElement> & {
		class?: string;
		level?: 1 | 2 | 3 | 4 | 5 | 6;
	};

	let className: $$Props["class"] = undefined;
	export { className as class };
	export let level: $$Props["level"] = 3;
</script>

{#if level === 1}
	<h1 class={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...$$restProps}>
		<slot />
	</h1>
{:else if level === 2}
	<h2 class={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...$$restProps}>
		<slot />
	</h2>
{:else if level === 3}
	<h3 class={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...$$restProps}>
		<slot />
	</h3>
{:else if level === 4}
	<h4 class={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...$$restProps}>
		<slot />
	</h4>
{:else if level === 5}
	<h5 class={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...$$restProps}>
		<slot />
	</h5>
{:else if level === 6}
	<h6 class={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...$$restProps}>
		<slot />
	</h6>
{/if}