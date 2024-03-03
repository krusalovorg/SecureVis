import App from './App';
import Header from './components/Header';
import VerticalHeader from './components/VerticalHeader';
import { BrowserRouter, Route, Router, Routes } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { UserData, getCookieToken, getUserData } from './utils/backend';
import Login from './pages/Login';
import Profile from './pages/Profile';
import User from './contexts/UserContext';
import Camera from './pages/Camera';
import Enterprises from './pages/Enterprises';
import Staff from './pages/Staff';
import LogsPage from './pages/Logs';

function RouterNav() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userData, setUserData] = useState<UserData | null>(null);
    const [token, setToken] = useState<null | string>(null);

    async function loadData(token: string) {
        const data = await getUserData(token);
        console.log(data);
        setUserData(data);
    }

    useEffect(() => {
        const get_token = getCookieToken();
        setIsLoggedIn(get_token ? true : false)
        if (get_token) {
            setToken(get_token);
            loadData(get_token);
        }
    }, [])

    return (
        <>
            <BrowserRouter>
                {
                    (isLoggedIn && token) ? <>
                        <User.Provider value={(userData || {}) as UserData}>
                            <Header />
                            <VerticalHeader>
                                <Routes>
                                    <Route path='/' element={<App />} />
                                    <Route path='*' element={<App />} />
                                    <Route path='/user' element={<Profile />} />
                                    <Route path='/camera' element={<Camera />} />
                                    <Route path='/enterprises' element={<Enterprises />} />
                                    <Route path='/staff' element={<Staff />} />
                                    <Route path='/logs' element={<LogsPage />} />
                                </Routes>
                            </VerticalHeader>
                        </User.Provider>
                    </>
                        :
                        <>
                            <Header />
                            <Routes>
                                <Route path='/login' element={<Login />} />
                                <Route path='/reg' element={<Login reg />} />
                                <Route path='*' element={<Login />} />
                            </Routes>
                        </>
                }
            </BrowserRouter>
        </>
    )
}

export default RouterNav;