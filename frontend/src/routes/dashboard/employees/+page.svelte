<script>
    import {onMount} from 'svelte';
    import {SvelteSet} from 'svelte/reactivity';
    import {fetchEmployees} from '$lib/api/employees';

    // UI Components
    import Button from '$lib/components/ui/button/button.svelte';
    import Input from '$lib/components/ui/input/input.svelte';
    import Checkbox from '$lib/components/ui/checkbox/checkbox.svelte';
    import Table from '$lib/components/ui/table/table.svelte';
    import TableBody from '$lib/components/ui/table/table-body.svelte';
    import TableCell from '$lib/components/ui/table/table-cell.svelte';
    import TableHead from '$lib/components/ui/table/table-head.svelte';
    import TableHeader from '$lib/components/ui/table/table-header.svelte';
    import TableRow from '$lib/components/ui/table/table-row.svelte';
    import DropdownMenu from '$lib/components/ui/dropdown-menu/dropdown-menu.svelte';
    import DropdownMenuTrigger from '$lib/components/ui/dropdown-menu/dropdown-menu-trigger.svelte';
    import DropdownMenuContent from '$lib/components/ui/dropdown-menu/dropdown-menu-content.svelte';
    import DropdownMenuCheckboxItem from '$lib/components/ui/dropdown-menu/dropdown-menu-checkbox-item.svelte';
    import DropdownMenuLabel from '$lib/components/ui/dropdown-menu/dropdown-menu-label.svelte';
    import DropdownMenuSeparator from '$lib/components/ui/dropdown-menu/dropdown-menu-separator.svelte';
    import * as Select from '$lib/components/ui/select';

    // Reactive state
    let allEmployees = $state([]);
    let loading = $state(true);
    let error = $state(null);

    // Table state
    let searchTerm = $state('');
    let currentPage = $state(1);
    let pageSize = $state(50);
    let sortColumn = $state('');
    let sortDirection = $state('asc'); // 'asc' | 'desc'
    let selectedEmployees = new SvelteSet();

    // Column visibility state
    let columnVisibility = $state({
        fullname: true,
        role: true,
        username: true,
        division: true,
        position: true,
        head: true,
        email: true,
        is_trainee: true,
        is_casino_allowed: false,
        is_exchange_banned: false
    });

    // Filter state
    let filters = $state({
        role: '',
        division: '',
        position: '',
        is_trainee: '',
        is_casino_allowed: '',
        is_exchange_banned: ''
    });

    // Computed filtered and sorted data
    let filteredEmployees = $derived.by(() => {
        let result = allEmployees;

        // Apply search filter
        if (searchTerm.trim()) {
            const search = searchTerm.toLowerCase();
            result = result.filter(employee =>
                employee.fullname?.toLowerCase().includes(search) ||
                employee.username?.toLowerCase().includes(search) ||
                employee.email?.toLowerCase().includes(search) ||
                employee.division?.toLowerCase().includes(search) ||
                employee.position?.toLowerCase().includes(search)
            );
        }

        // Apply column filters
        if (filters.division) {
            result = result.filter(emp => emp.division === filters.division);
        }

        if (filters.is_trainee !== '') {
            result = result.filter(emp => emp.is_trainee === (filters.is_trainee === 'true'));
        }

        if (filters.is_casino_allowed !== '') {
            result = result.filter(emp => emp.is_casino_allowed === (filters.is_casino_allowed === 'true'));
        }

        if (filters.is_exchange_banned !== '') {
            result = result.filter(emp => emp.is_exchange_banned === (filters.is_exchange_banned === 'true'));
        }

        // Apply sorting
        if (sortColumn) {
            result = [...result].sort((a, b) => {
                const aVal = a[sortColumn];
                const bVal = b[sortColumn];

                if (aVal === null || aVal === undefined) return 1;
                if (bVal === null || bVal === undefined) return -1;

                let comparison = 0;
                if (typeof aVal === 'string' && typeof bVal === 'string') {
                    comparison = aVal.localeCompare(bVal);
                } else {
                    comparison = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
                }

                return sortDirection === 'desc' ? -comparison : comparison;
            });
        }

        return result;
    });

    // Computed paginated data
    let paginatedEmployees = $derived.by(() => {
        const startIndex = (currentPage - 1) * pageSize;
        const endIndex = startIndex + pageSize;
        return filteredEmployees.slice(startIndex, endIndex);
    });

    // Computed pagination info
    let totalPages = $derived(Math.ceil(filteredEmployees.length / pageSize));
    let startRow = $derived((currentPage - 1) * pageSize + 1);
    let endRow = $derived(Math.min(currentPage * pageSize, filteredEmployees.length));

    // Get unique values for filter dropdowns
    let uniqueDivisions = $derived.by(() => {
        const divisions = new Set(allEmployees.map(emp => emp.division).filter(Boolean));
        return Array.from(divisions).sort();
    });
    let uniquePositions = $derived.by(() => {
        const positions = new Set(allEmployees.map(emp => emp.position).filter(Boolean));
        return Array.from(positions).sort();
    });
    let uniqueRoles = $derived.by(() => {
        const roles = new Set(allEmployees.map(emp => emp.role).filter(Boolean));
        return Array.from(roles).sort((a, b) => a - b);
    });

    // Load employees data
    onMount(async () => {
        try {
            loading = true;
            // Get auth token from page data or wherever it's stored
            const token = localStorage.getItem('access_token') || '';
            const result = await fetchEmployees(token);
            allEmployees = result.employees;
        } catch (err) {
            error = err.message;
            console.error('Error loading employees:', err);
        } finally {
            loading = false;
        }
    });

    // Sorting functions
    function toggleSort(column) {
        if (sortColumn === column) {
            sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            sortColumn = column;
            sortDirection = 'asc';
        }
        currentPage = 1; // Reset to first page when sorting
    }


    // Selection functions
    function toggleSelectAll(checked) {
        if (checked) {
            paginatedEmployees.forEach(emp => selectedEmployees.add(emp.id));
        } else {
            paginatedEmployees.forEach(emp => selectedEmployees.delete(emp.id));
        }
        // SvelteSet is already reactive
    }

    function toggleSelectEmployee(id, checked) {
        if (checked) {
            selectedEmployees.add(id);
        } else {
            selectedEmployees.delete(id);
        }
    }

    function isAllSelected() {
        return paginatedEmployees.length > 0 && paginatedEmployees.every(emp => selectedEmployees.has(emp.id));
    }

    function isSomeSelected() {
        return paginatedEmployees.some(emp => selectedEmployees.has(emp.id));
    }

    // Pagination functions

    function nextPage() {
        if (currentPage < totalPages) {
            currentPage++;
        }
    }

    function previousPage() {
        if (currentPage > 1) {
            currentPage--;
        }
    }

    // Reset filters
    function resetFilters() {
        searchTerm = '';
        filters = {
            role: '',
            division: '',
            position: '',
            is_trainee: '',
            is_casino_allowed: '',
            is_exchange_banned: ''
        };
        currentPage = 1;
    }
</script>

<div class="w-full space-y-4">
    <div class="flex items-center justify-between">
        <h1 class="text-2xl font-semibold tracking-tight">Сотрудники</h1>
    </div>

    {#if loading}
        <div class="flex items-center justify-center py-8">
            <p>Загрузка...</p>
        </div>
    {:else if error}
        <div class="flex items-center justify-center py-8 text-red-600">
            <p>Ошибка загрузки: {error}</p>
        </div>
    {:else}
        <!-- Controls -->
        <div class="flex items-center justify-between gap-4">
            <div class="flex flex-1 items-center gap-4">
                <!-- Search -->
                <Input
                        placeholder="Поиск сотрудников..."
                        bind:value={searchTerm}
                        class="max-w-sm"
                />

                <!-- Division filter -->
                {#if uniqueDivisions.length > 0}
                    <Select.Root bind:value={filters.division}>
                        <Select.Trigger class="w-45">
                            {filters.division || 'Все подразделения'}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Group>
                                <Select.Label>Подразделения</Select.Label>
                                <Select.Item value="">Все подразделения</Select.Item>
                                {#each uniqueDivisions as division (division)}
                                    <Select.Item value={division}>
                                        {division}
                                    </Select.Item>
                                {/each}
                            </Select.Group>
                        </Select.Content>
                    </Select.Root>
                {/if}

                <!-- Position filter -->
                {#if uniquePositions.length > 0}
                    <Select.Root bind:value={filters.position}>
                        <Select.Trigger class="w-45">
                            {filters.position || 'Все должности'}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Group>
                                <Select.Label>Должности</Select.Label>
                                <Select.Item value="">Все должности</Select.Item>
                                {#each uniquePositions as position (position)}
                                    <Select.Item value={position}>
                                        {position}
                                    </Select.Item>
                                {/each}
                            </Select.Group>
                        </Select.Content>
                    </Select.Root>
                {/if}

                <!-- Role filter -->
                {#if uniqueRoles.length > 0}
                    <Select.Root bind:value={filters.role}>
                        <Select.Trigger class="w-45">
                            {filters.position || 'Все роли'}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Group>
                                <Select.Label>Роли</Select.Label>
                                <Select.Item value="">Все роли</Select.Item>
                                {#each uniqueRoles as role (role)}
                                    <Select.Item value={role}>
                                        {role}
                                    </Select.Item>
                                {/each}
                            </Select.Group>
                        </Select.Content>
                    </Select.Root>
                {/if}

                <!-- Reset filters -->
                {#if searchTerm || filters.role || filters.division || filters.position || filters.is_trainee !== '' || filters.is_casino_allowed !== '' || filters.is_exchange_banned !== ''}
                    <Button variant="outline" onclick={resetFilters}>
                        Сбросить фильтры
                    </Button>
                {/if}
            </div>

            <!-- Column visibility -->
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    {#snippet children({builder})}
                        <Button variant="outline" builders={[builder]} class="ml-auto">
                            Колонки
                            ▼
                        </Button>
                    {/snippet}
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" class="w-48">
                    <DropdownMenuLabel>Показать колонки</DropdownMenuLabel>
                    <DropdownMenuSeparator/>
                    {#each Object.entries(columnVisibility) as [column, visible] (column)}
                        <DropdownMenuCheckboxItem
                                bind:checked={columnVisibility[column]}
                                class="capitalize"
                        >
                            {column.replace('_', ' ')}
                        </DropdownMenuCheckboxItem>
                    {/each}
                </DropdownMenuContent>
            </DropdownMenu>
        </div>

        <!-- Table -->
        <div class="rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <!-- Select All -->
                        <TableHead class="w-12">
                            <Checkbox
                                    checked={isAllSelected()}
                                    indeterminate={!isAllSelected() && isSomeSelected()}
                                    onCheckedChange={toggleSelectAll}
                                    aria-label="Select all"
                            />
                        </TableHead>

                        {#if columnVisibility.fullname}
                            <TableHead>
                                <Button variant="ghost" onclick={() => toggleSort('fullname')}>
                                    ФИО
                                    {#if sortColumn === 'fullname'}
                                        {#if sortDirection === 'asc'}
                                            ↑
                                        {:else}
                                            ↓
                                        {/if}
                                    {:else}
                                        ↕
                                    {/if}
                                </Button>
                            </TableHead>
                        {/if}

                        {#if columnVisibility.role}
                            <TableHead>
                                <Button variant="ghost" onclick={() => toggleSort('role')}>
                                    Роль
                                    {#if sortColumn === 'role'}
                                        {#if sortDirection === 'asc'}
                                            ↑
                                        {:else}
                                            ↓
                                        {/if}
                                    {:else}
                                        ↕
                                    {/if}
                                </Button>
                            </TableHead>
                        {/if}

                        {#if columnVisibility.username}
                            <TableHead>
                                <Button variant="ghost" onclick={() => toggleSort('username')}>
                                    Username
                                    {#if sortColumn === 'username'}
                                        {#if sortDirection === 'asc'}
                                            ↑
                                        {:else}
                                            ↓
                                        {/if}
                                    {:else}
                                        ↕
                                    {/if}
                                </Button>
                            </TableHead>
                        {/if}

                        {#if columnVisibility.division}
                            <TableHead>
                                <Button variant="ghost" onclick={() => toggleSort('division')}>
                                    Подразделение
                                    {#if sortColumn === 'division'}
                                        {#if sortDirection === 'asc'}
                                            ↑
                                        {:else}
                                            ↓
                                        {/if}
                                    {:else}
                                        ↕
                                    {/if}
                                </Button>
                            </TableHead>
                        {/if}

                        {#if columnVisibility.position}
                            <TableHead>
                                <Button variant="ghost" onclick={() => toggleSort('position')}>
                                    Должность
                                    {#if sortColumn === 'position'}
                                        {#if sortDirection === 'asc'}
                                            ↑
                                        {:else}
                                            ↓
                                        {/if}
                                    {:else}
                                        ↕
                                    {/if}
                                </Button>
                            </TableHead>
                        {/if}

                        {#if columnVisibility.head}
                            <TableHead>
                                <Button variant="ghost" onclick={() => toggleSort('head')}>
                                    Руководитель
                                    {#if sortColumn === 'head'}
                                        {#if sortDirection === 'asc'}
                                            ↑
                                        {:else}
                                            ↓
                                        {/if}
                                    {:else}
                                        ↕
                                    {/if}
                                </Button>
                            </TableHead>
                        {/if}

                        {#if columnVisibility.email}
                            <TableHead>
                                <Button variant="ghost" onclick={() => toggleSort('email')}>
                                    Email
                                    {#if sortColumn === 'email'}
                                        {#if sortDirection === 'asc'}
                                            ↑
                                        {:else}
                                            ↓
                                        {/if}
                                    {:else}
                                        ↕
                                    {/if}
                                </Button>
                            </TableHead>
                        {/if}

                        {#if columnVisibility.is_trainee}
                            <TableHead>Стажёр</TableHead>
                        {/if}

                        {#if columnVisibility.is_casino_allowed}
                            <TableHead>Казино разрешено</TableHead>
                        {/if}

                        {#if columnVisibility.is_exchange_banned}
                            <TableHead>Обмен запрещён</TableHead>
                        {/if}

                        <TableHead class="w-12"></TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {#if paginatedEmployees.length}
                        {#each paginatedEmployees as employee (employee.id)}
                            <TableRow class={selectedEmployees.has(employee.id) ? 'bg-muted/50' : ''}>
                                <!-- Select Row -->
                                <TableCell>
                                    <Checkbox
                                            checked={selectedEmployees.has(employee.id)}
                                            onCheckedChange={(checked) => toggleSelectEmployee(employee.id, checked)}
                                            aria-label="Select row"
                                    />
                                </TableCell>

                                {#if columnVisibility.id}
                                    <TableCell>{employee.id}</TableCell>
                                {/if}

                                {#if columnVisibility.fullname}
                                    <TableCell class="font-medium">{employee.fullname}</TableCell>
                                {/if}

                                {#if columnVisibility.role}
                                    <TableCell>{employee.role}</TableCell>
                                {/if}

                                {#if columnVisibility.username}
                                    <TableCell>{employee.username || ''}</TableCell>
                                {/if}

                                {#if columnVisibility.division}
                                    <TableCell>{employee.division || ''}</TableCell>
                                {/if}

                                {#if columnVisibility.position}
                                    <TableCell>{employee.position || ''}</TableCell>
                                {/if}

                                {#if columnVisibility.head}
                                    <TableCell>{employee.head || ''}</TableCell>
                                {/if}

                                {#if columnVisibility.email}
                                    <TableCell>{employee.email || ''}</TableCell>
                                {/if}

                                {#if columnVisibility.is_trainee}
                                    <TableCell>
										<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {employee.is_trainee ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">
											{employee.is_trainee ? 'Да' : 'Нет'}
										</span>
                                    </TableCell>
                                {/if}

                                {#if columnVisibility.is_casino_allowed}
                                    <TableCell>
										<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {employee.is_casino_allowed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
											{employee.is_casino_allowed ? 'Да' : 'Нет'}
										</span>
                                    </TableCell>
                                {/if}

                                {#if columnVisibility.is_exchange_banned}
                                    <TableCell>
										<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {employee.is_exchange_banned ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}">
											{employee.is_exchange_banned ? 'Да' : 'Нет'}
										</span>
                                    </TableCell>
                                {/if}

                                <!-- Actions -->
                                <TableCell>
                                    <DropdownMenu>
                                        <DropdownMenuTrigger asChild>
                                            {#snippet children({builder})}
                                                <Button variant="ghost" builders={[builder]} size="sm"
                                                        class="h-8 w-8 p-0">
                                                    <span class="sr-only">Открыть меню</span>
                                                    ⋯
                                                </Button>
                                            {/snippet}
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuLabel>Действия</DropdownMenuLabel>
                                            <DropdownMenuSeparator/>
                                            <button class="w-full px-2 py-1.5 text-sm text-left hover:bg-accent"
                                                    onclick={() => navigator.clipboard.writeText(employee.id.toString())}>
                                                Копировать ID
                                            </button>
                                            <button class="w-full px-2 py-1.5 text-sm text-left hover:bg-accent">
                                                Просмотр сотрудника
                                            </button>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </TableCell>
                            </TableRow>
                        {/each}
                    {:else}
                        <TableRow>
                            <TableCell colspan="12" class="h-24 text-center">
                                {searchTerm ? 'Сотрудники не найдены.' : 'Нет данных.'}
                            </TableCell>
                        </TableRow>
                    {/if}
                </TableBody>
            </Table>
        </div>

        <!-- Pagination -->
        {#if filteredEmployees.length > 0}
            <div class="flex items-center justify-between space-x-2 py-4">
                <div class="text-sm text-muted-foreground">
                    {selectedEmployees.size} из {filteredEmployees.length} строк выбрано.
                    Показано {startRow}{endRow} из {filteredEmployees.length} записей.
                </div>

                <div class="flex items-center space-x-2">
                    <div class="flex items-center space-x-2">
                        <p class="text-sm font-medium">Строк на странице</p>
                        <select bind:value={pageSize} class="px-3 py-1 border rounded">
                            <option value={25}>25</option>
                            <option value={50}>50</option>
                            <option value={100}>100</option>
                        </select>
                    </div>

                    <div class="flex items-center space-x-2">
                        <p class="text-sm font-medium">
                            Страница {currentPage} из {totalPages}
                        </p>
                        <div class="flex items-center space-x-1">
                            <Button
                                    variant="outline"
                                    size="sm"
                                    onclick={previousPage}
                                    disabled={currentPage <= 1}
                            >
                                Назад
                            </Button>
                            <Button
                                    variant="outline"
                                    size="sm"
                                    onclick={nextPage}
                                    disabled={currentPage >= totalPages}
                            >
                                Вперёд
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    {/if}
</div>
