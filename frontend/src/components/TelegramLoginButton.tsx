import {LoginButton} from "@telegram-auth/react";
import {useAuth} from '../contexts/AuthContext';

export function TelegramLoginButton() {
    const { login } = useAuth();

    const handleAuthCallback = async (data: any) => {
        console.log(`Authorized by ${data.username}`);
        await login(data);
    };

    return (
        <div className="telegram-login-container">
            <LoginButton
                botUsername={import.meta.env.VITE_BOT_NAME}
                onAuthCallback={handleAuthCallback}
                buttonSize="medium"
                showAvatar={true}
                lang="ru"
            />
        </div>
    );
}
