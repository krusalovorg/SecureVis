import { useContext, useEffect, useRef, useState } from "react";
import { URL_SERVER, getCookieToken, getImage } from "../utils/backend";
import Input from "../components/Input";
import UserContext from "../contexts/UserContext";
import io from 'socket.io-client';

function Camera() {
    const userData = useContext(UserContext);
    const videoRef = useRef<HTMLImageElement>(null);
    
    const socket = io(URL_SERVER, {
        autoConnect: false,
    });


    useEffect(() => {
        if (userData) {

        }
        console.log('usetrdata', userData)
    }, [userData])

    useEffect(() => {
        socket.connect();
        socket.on('frame', (data: any) => {
            console.log(data)
            if (videoRef.current && videoRef.current.src) {
                videoRef.current.src = `data:image/jpeg;base64,${data.image}`;
            }
        });

        socket.on('connect', (data: any) => {
            console.log(data)
            socket.emit("connect", 'ffffffff')
        })

        return () => {
            socket.disconnect();
        };
    }, []);

    return (
        <div className="w-full h-full flex justify-center align-center">
            <div className="w-full h-full flex justify-center items-center">
                <div className="w-[90%] h-[90%] bg-[#F5FAFD] rounded-3xl relative">
                    <div className="w-full bg-white h-[80px] rounded-t-3xl flex flex-row items-center px-5 mb-5">
                        <div className="ml-5 gap-2">
                            <h1 className={`text-xl text-black font-[Montserrat]`}>
                                Ваша камера
                            </h1>
                        </div>
                    </div>
                    <div className="px-[3%] pt-2 flex flex-row w-full">
                        <img ref={videoRef} alt="Video stream" />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Camera;