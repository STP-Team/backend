import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';

interface UserInfo {
    user_id: number;
    fullname: string;
    role: number;
    username?: string;
    division?: string;
    position?: string;
}

interface AuthContextType {
    isAuthenticated: boolean;
    userInfo: UserInfo | null;
    loading: boolean;
    login: (telegramData: any) => Promise<void>;
    logout: () => void;
    checkAuthStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
    const [loading, setLoading] = useState(true);

    // Check if user is already authenticated on provider mount
    useEffect(() => {
        void checkAuthStatus();
    }, []);

    const checkAuthStatus = async () => {
        const token = getCookie('access_token');
        if (token) {
            try {
                const response = await axios.get(`http://localhost:8000/api/v1/auth/me`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setUserInfo(response.data);
                setIsAuthenticated(true);
            } catch (error) {
                // Token is invalid, remove it
                deleteCookie('access_token');
            }
        }
        setLoading(false);
    };

    const login = async (telegramData: any) => {
        try {
            setLoading(true);

            // Prepare auth data according to TelegramAuthData schema
            const authData = {
                id: String(telegramData.id),
                first_name: telegramData.first_name,
                last_name: telegramData.last_name || '',
                username: telegramData.username || '',
                photo_url: telegramData.photo_url || '',
                auth_date: String(telegramData.auth_date),
                hash: telegramData.hash
            };

            const response = await axios.post(`http://localhost:8000/api/v1/auth/telegram`, authData);

            const { access_token } = response.data;

            // Store token in cookies with actual token expiry
            const tokenExpiry = getTokenExpiryInDays(access_token);
            setCookie('access_token', access_token, tokenExpiry);

            // Get user info
            const userResponse = await axios.get(`http://localhost:8000/api/v1/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${access_token}`
                }
            });

            setUserInfo(userResponse.data);
            setIsAuthenticated(true);

        } catch (error) {
            console.error('Authentication failed:', error);
            if (error && typeof error === 'object' && 'response' in error) {
                const axiosError = error as any;
                if (axiosError.response?.data?.detail) {
                    alert(`Authentication failed: ${axiosError.response.data.detail}`);
                } else {
                    alert('Authentication failed. Please try again.');
                }
            } else {
                alert('Authentication failed. Please try again.');
            }
            throw error;
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        deleteCookie('access_token');
        setIsAuthenticated(false);
        setUserInfo(null);
    };

    // JWT helper function
    const getTokenExpiryInDays = (token: string): number => {
        try {
            // Decode JWT payload (we only need the payload, not verification)
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(
                atob(base64)
                    .split('')
                    .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                    .join('')
            );

            const decoded = JSON.parse(jsonPayload);
            const exp = decoded.exp; // Expiration timestamp in seconds

            if (!exp) {
                console.warn('Token has no expiration, using 1 day default');
                return 1;
            }

            const now = Math.floor(Date.now() / 1000); // Current timestamp in seconds
            const secondsUntilExpiry = exp - now;
            return Math.max(0, Math.ceil(secondsUntilExpiry / (24 * 60 * 60)));
        } catch (error) {
            console.error('Failed to decode token expiry:', error);
            return 1;
        }
    };

    // Cookie helper functions
    const setCookie = (name: string, value: string, days: number) => {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
    };

    const getCookie = (name: string): string | null => {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    };

    const deleteCookie = (name: string) => {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    };

    const value = {
        isAuthenticated,
        userInfo,
        loading,
        login,
        logout,
        checkAuthStatus
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};