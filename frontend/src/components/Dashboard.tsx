import {useAuth} from '../contexts/AuthContext';

export function Dashboard() {
    const {userInfo, logout} = useAuth();

    if (!userInfo) {
        return null;
    }

    return (
        <div className="dashboard">
            <div style={{padding: '20px', textAlign: 'center'}}>
                <h2>СТП | Панель управления</h2>
                <div style={{marginBottom: '20px'}}>
                    <h3>Информация о пользователе</h3>
                    <p><strong>ФИО:</strong> {userInfo.fullname}</p>
                    {userInfo.username && <p><strong>Username:</strong> @{userInfo.username}</p>}
                    {userInfo.position && <p><strong>Должность:</strong> {userInfo.position}</p>}
                    {userInfo.division && <p><strong>Направление:</strong> {userInfo.division}</p>}
                    <p><strong>User ID:</strong> {userInfo.user_id}</p>
                    <p><strong>Роль:</strong> {userInfo.role}</p>
                </div>
                <button
                    onClick={logout}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: '#dc3545',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        marginTop: '20px'
                    }}
                >
                    Выйти
                </button>
            </div>
        </div>
    );
}