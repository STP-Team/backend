import {writable} from 'svelte/store';
import type {UserInfo} from '../auth.js';

interface AuthState {
    isAuthenticated: boolean;
    user: UserInfo | null;
    token: string | null;
    loading: boolean;
    error: string | null;
    lastValidated?: number;
}

const initialState: AuthState = {
    isAuthenticated: false,
    user: null,
    token: null,
    loading: false,
    error: null,
};

export const authStore = writable<AuthState>(initialState);

export const authActions = {
    setLoading: (loading: boolean) => {
        authStore.update(state => ({...state, loading, error: null}));
    },

    setError: (error: string) => {
        authStore.update(state => ({...state, error, loading: false}));
    },

    setAuthenticated: (user: UserInfo, token: string) => {
        authStore.update(state => ({
            ...state,
            isAuthenticated: true,
            user,
            token,
            loading: false,
            error: null,
            lastValidated: Date.now(),
        }));
    },

    logout: () => {
        authStore.set(initialState);
    }
};