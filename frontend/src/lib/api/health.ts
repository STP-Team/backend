const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface HealthStatus {
	status: 'healthy' | 'unhealthy' | 'unknown';
	timestamp: number;
	details?: string;
}

export async function checkApiHealth(): Promise<HealthStatus> {
	try {
		const response = await fetch(`${API_BASE_URL}/health`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			},
			signal: AbortSignal.timeout(5000) // 5 second timeout
		});

		if (response.ok) {
			return {
				status: 'healthy',
				timestamp: Date.now()
			};
		} else {
			return {
				status: 'unhealthy',
				timestamp: Date.now(),
				details: `HTTP ${response.status}`
			};
		}
	} catch (error) {
		return {
			status: 'unhealthy',
			timestamp: Date.now(),
			details: error instanceof Error ? error.message : 'Unknown error'
		};
	}
}
