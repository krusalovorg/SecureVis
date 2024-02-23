import { useContext } from "react";
import UserContext from "../contexts/UserContext";
import { getImage } from "../utils/backend";
import { useNavigate } from "react-router-dom";
import UserIcon from '../icons/user.svg';

function Header() {
    const userData = useContext(UserContext);
    const navigate = useNavigate();

    return (
        <header className="h-[68px] flex flex-row justify-between items-center px-5 py-2 bg-white shadow-md fixed top-0 left-0 w-full z-[100]">
            <svg width="24" height="24" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6.7999 9.1999L9.79935 7.07175L16.3999 1.9999M10.9999 6.1999L19.9999 12.1999M15.1999 9.7999L12.1999 19.9999M13.3999 14.5999H1.9999M8.5999 14.5999L3.7999 1.9999M6.1999 20.5999H15.7999C18.4509 20.5999 20.5999 18.4509 20.5999 15.7999V6.1999C20.5999 3.54894 18.4509 1.3999 15.7999 1.3999H6.1999C3.54894 1.3999 1.3999 3.54894 1.3999 6.1999V15.7999C1.3999 18.4509 3.54894 20.5999 6.1999 20.5999Z" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>

            <h1 className="text-black font-semibold mr-auto ml-5">Система безопасной визуальной идентификации</h1>
            {userData?.name &&
                <div className="flex flex-row items-center cursor-pointer" onClick={() => navigate('/user')}>
                    <h1 className="text-black font-semibold">{userData.surname} {userData.name}</h1>
                    <img
                        src={UserIcon}
                        className="w-[42px] h-[42px] rounded-full ml-2"
                    />
                </div>
            }
        </header>
    )
}

export default Header;