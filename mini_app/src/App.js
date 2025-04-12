import { useState, useEffect } from 'react'; // Добавляем хуки
import logo from './logo.svg';
import './App.css';

function App() {
    const [userData, setUserData] = useState(null); // Состояние для хранения данных

    useEffect(() => {
        const data = window.Telegram.WebApp.initData;

        fetch('/api/telegram/mini_app/auth/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'tma ' + data,
                'accept': '*/*',
                'X-CSRFTOKEN': 'kC4TIa7u6DtPupR4HRz8oCcSeQaeRLBaZ5oSHAKdUJD0oqroGSrgcG49ygN523QF',
            }
        })
            .then(response => response.json())
            .then(result => {
                setUserData(result.user); // Обновляем состояние
                console.log('Данные пользователя:', result.user); // Логируем результат
            })
            .catch(error => console.error('Ошибка:', error));
    }, []); // Пустой массив зависимостей = запрос выполнится 1 раз при загрузке

    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <h1>
                    {userData ? JSON.stringify(userData) : 'Загрузка...'}
                </h1>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a>
            </header>
        </div>
    );
}

export default App;
