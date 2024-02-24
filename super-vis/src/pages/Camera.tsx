import { useContext, useEffect, useRef, useState } from "react";
import { URL_SERVER, getCookieToken, getImage } from "../utils/backend";
import Input from "../components/Input";
import UserContext from "../contexts/UserContext";

function Camera() {
    const userData = useContext(UserContext);
    const videoRef = useRef<HTMLImageElement>(null);

    useEffect(() => {
        if (userData._id) {
            const socket = new WebSocket('ws://127.0.0.1:5001/connect'); // Замените на адрес вашего сервера

            socket.onopen = () => {
                console.log('WebSocket connection established.');
                const apiId = userData._id; // Получите айди пользователя из контекста
                const connectData = { apiId: apiId }; // Создайте объект с айди
                console.log('send:::', JSON.stringify(connectData), apiId)
                socket.send(JSON.stringify(connectData))
            };

            socket.onmessage = async (event) => {
                // Обработка полученных видеокадров (например, отображение в элементе video)
                console.log('Received video:', event.data);

                const base64String = event.data;
                const byteArray = new Uint8Array(atob(base64String).split('').map(char => char.charCodeAt(0)));

                // Создаем Blob из массива байт
                const blob = new Blob([byteArray], { type: 'image/jpeg' });

                // Создаем URL из Blob
                const imageUrl = URL.createObjectURL(blob);
                console.log('imageUrl', imageUrl);

                if (videoRef.current) {
                    videoRef.current.src = imageUrl;
                }
            };

            socket.onclose = () => {
                console.log('WebSocket connection closed.');
            };

            // Clean up when component unmounts
            // return () => {
            //   socket.close();
            // };
        }
    }, [userData]);

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
                        <img ref={videoRef} className="w-full h-full" alt="Video stream" />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Camera;