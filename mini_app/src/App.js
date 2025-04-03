import logo from './logo.svg';
import './App.css';

function App() {
  const data = window.Telegram.WebApp.initData
  let userData

    fetch('http://egame-lyceum.ru:3333/api/telegram/auth/verify', {
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
        userData = result.user;
    })
    .catch(error => console.error('Error:', error));

        return (
        <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          {userData}
        </p>
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
