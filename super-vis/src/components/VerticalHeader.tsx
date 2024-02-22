import { useNavigate } from 'react-router-dom';
import MailIcon from '../icons/mail.svg';
import Mail from '../icons/Mail';
import User from '../icons/User';
import Logout from '../icons/Logout';
import { logout } from '../utils/backend';
import FileIcon from '../icons/FileIcon';
import PenWrite from '../icons/PenWrite';

function VerticalHeader({ children }: any) {
    const navigate = useNavigate();
    const url = window.location.pathname;

    return (
        <div className="h-screen flex flex-row align-top z-[99]">
            <header className="w-[100px] h-full flex fixed left-0 flex-col justify-start items-center px-5 bg-white shadow-sm pt-[80px]">
                <div onClick={() => navigate("/user")} className={`p-[20px] rounded-full cursor-pointer ${url == '/user' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <User />
                </div>
                <div onClick={() => navigate("/chats")} className={`p-[20px] rounded-full cursor-pointer ${url == '/chats' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <Mail />
                </div>
                <div onClick={() => navigate("/references")} className={`p-[20px] rounded-full cursor-pointer ${url == '/references' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <FileIcon />
                </div>
                <div onClick={() => navigate("/history")} className={`p-[20px] rounded-full cursor-pointer ${url == '/history' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <PenWrite />
                </div>
                <div onClick={() => logout()} className={`p-[20px] rounded-full cursor-pointer mt-auto mb-2 text-black`} >
                    <Logout />
                </div>
            </header>
            <div className='w-[100px]'></div>
            <div className='w-full pt-[68px]'>
                {children}
            </div>
        </div>
    )
}

export default VerticalHeader;