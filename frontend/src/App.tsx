import './App.css'
import {AuthProvider, useAuth} from './contexts/AuthContext';
import {TelegramLoginButton} from "./components/TelegramLoginButton";
import {Dashboard} from "./components/Dashboard";

function AppContent() {
    const {isAuthenticated, loading} = useAuth();

    if (loading) {
        return (
            <div className="loading-container" style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh'
            }}>
                <div>Загрузка...</div>
            </div>
        );
    }

    return (
        <div className="app-content">
            {isAuthenticated ? (
                <Dashboard/>
            ) : (
                <div className="card">
                    <TelegramLoginButton/>
                </div>
            )}
        </div>
    );
}

function App() {
    return (
        <AuthProvider>
            <AppContent/>
        </AuthProvider>
    );
}

export default App
