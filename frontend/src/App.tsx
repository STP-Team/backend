import './App.css'
import {LoginButton} from '@telegram-auth/react';
import {checkUserAccess} from "./scripts/auth.tsx";


function App() {

    return (
        <>
            <div className="telegram-auth">
                <p>Для доступа требуется авторизация</p>
                <div className="App">
                    <LoginButton
                        botUsername="stpsher_testbot"
                        buttonSize="large"
                        cornerRadius={5}
                        showAvatar={true}
                        lang="ru"
                        onAuthCallback={async (data) => {
                            console.log('Telegram auth data:', data);

                            if (data.id) {
                                try {
                                    const userCheck = await checkUserAccess(data.id);

                                    if (userCheck.hasAccess) {
                                        alert(`Привет, ${userCheck.fullname}. Твоя роль: ${userCheck.role}`);
                                    } else {
                                        alert('Доступ запрещен. Пользователь не найден в системе или не имеет необходимых прав.');
                                    }
                                } catch (error) {
                                    console.error('Authorization error:', error);
                                    alert('Произошла ошибка при проверке авторизации. Попробуйте еще раз.');
                                }
                            } else {
                                alert('Ошибка авторизации: не получен идентификатор пользователя.');
                            }
                        }}
                    />
                </div>
            </div>
        </>
    )
}

export default App
