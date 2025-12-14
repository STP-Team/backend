// Auth utility functions and types
export interface TelegramAuthData {
    id: string;
    first_name: string;
    last_name?: string;
    username?: string;
    photo_url?: string;
    auth_date: string;
    hash: string;
}

export interface TokenInfo {
    access_token: string;
    token_type: string;
}

export interface UserInfo {
    user_id: number;
    fullname: string;
    role: number;
    username?: string;
    division?: string;
    position?: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

/**
 * Authenticate with Telegram data
 */
export async function authenticateTelegram(authData: TelegramAuthData): Promise<TokenInfo> {
    const response = await fetch(`${API_BASE_URL}/auth/telegram`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(authData),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Authentication failed');
    }

    return await response.json();
}

/**
 * Get current user info
 */
export async function getCurrentUser(token: string): Promise<UserInfo> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to get user info');
    }

    return await response.json();
}

/**
 * Store token in localStorage
 */
export function storeToken(token: string): void {
    localStorage.setItem('access_token', token);
}

/**
 * Get stored token from localStorage
 */
export function getStoredToken(): string | null {
    return localStorage.getItem('access_token');
}

/**
 * Remove token from localStorage
 */
export function removeToken(): void {
    localStorage.removeItem('access_token');
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
    return getStoredToken() !== null;
}