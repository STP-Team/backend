const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface Employee {
	id: number;
	fullname: string;
	role: number;
	user_id: number | null;
	username: string | null;
	division: string | null;
	position: string | null;
	head: string | null;
	email: string | null;
	is_trainee: boolean;
	is_casino_allowed: boolean;
	is_exchange_banned: boolean;
}

export interface EmployeesList {
	employees: Employee[];
}

export interface EmployeeFilters {
	main_id?: number;
	user_id?: number;
	username?: string;
	fullname?: string;
	email?: string;
	head?: string;
	roles?: number[];
}

export async function fetchEmployees(
	token: string,
	filters: EmployeeFilters = {}
): Promise<EmployeesList> {
	const params = new URLSearchParams();

	if (filters.main_id) params.append('main_id', filters.main_id.toString());
	if (filters.user_id) params.append('user_id', filters.user_id.toString());
	if (filters.username) params.append('username', filters.username);
	if (filters.fullname) params.append('fullname', filters.fullname);
	if (filters.email) params.append('email', filters.email);
	if (filters.head) params.append('head', filters.head);
	if (filters.roles) {
		filters.roles.forEach(role => params.append('roles', role.toString()));
	}

	const url = `${API_BASE_URL}/employees${params.toString() ? '?' + params.toString() : ''}`;

	try {
		const response = await fetch(url, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
			}
		});

		if (!response.ok) {
			if (response.status === 404) {
				return { employees: [] };
			}
			throw new Error(`HTTP ${response.status}: ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error('Error fetching employees:', error);
		throw error;
	}
}