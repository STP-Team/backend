import { writable } from 'svelte/store';

export interface Breadcrumb {
	label: string;
	href?: string;
}

export const breadcrumbsStore = writable<Breadcrumb[]>([]);

export function setBreadcrumbs(breadcrumbs: Breadcrumb[]) {
	breadcrumbsStore.set(breadcrumbs);
}

export function clearBreadcrumbs() {
	breadcrumbsStore.set([]);
}