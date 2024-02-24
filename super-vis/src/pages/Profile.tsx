import { useContext, useEffect, useState } from "react";
import { URL_SERVER, getCookieToken, getImage } from "../utils/backend";
import Input from "../components/Input";
import UserContext from "../contexts/UserContext";

function Profile() {
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [patronymic, setPatronymic] = useState('');

    const [email, setEmail] = useState('');

    const [errors, setErrors] = useState({
        name: '',
        surname: '',
        patronymic: '',
        city: '',
    });

    const [submited, setSubmited] = useState(false);

    const userData = useContext(UserContext);

    const checkErrors = (submited_local?: boolean) => {
        const fields = { name, surname, patronymic, email };
        let error = false;
        let errors_res = errors;
        for (const field in fields) {
            const value = (fields as any)[field];
            if (value?.length === 0) {
                console.log('Field', field, 'is empty');
                if (submited || submited_local) {
                    errors_res = { ...errors_res, [field]: "Поле не заполнено" }
                    error = true;
                }
            } else {
                errors_res = { ...errors_res, [field]: "" }
            }
        }
        setErrors(errors_res)
        return error;
    };

    useEffect(() => {
        checkErrors();
    }, [name, surname, patronymic, email])

    async function updateUserData() {
        setSubmited(true);
        const errors = checkErrors(true);
        if (!errors) {
            // if (file) {
            //     console.log("formData.images", file)
            //     new_userData.append('avatar', file, file.name);
            // }

            fetch(URL_SERVER + '/enterprise', {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + getCookieToken(),
                },
                body: JSON.stringify({ name, surname, patronymic, email })
            })
                .then(response => response.json())
                .then(data => {
                    console.log('User updated successfully:', data);
                    window.location.reload();
                })
                .catch(error => {
                    console.error('Error updating user:', error);
                });
        }
    }

    useEffect(() => {
        if (userData) {
            setName(userData?.name);
            setSurname(userData?.surname);
            setPatronymic(userData?.patronymic);
            setEmail(userData?.email);
        }
        console.log('usetrdata', userData)
    }, [userData])

    return (
        <div className="w-full h-full flex justify-center align-center">
            <div className="w-full h-full flex justify-center items-center">
                <div className="w-[90%] h-[90%] bg-[#F5FAFD] rounded-3xl relative">
                    <div className="w-full bg-white h-[80px] rounded-t-3xl flex flex-row items-center px-5 mb-5">
                        <div className="ml-5 gap-2">
                            <h1 className={`text-xl text-black font-[Montserrat]`}>
                                Ваш профиль
                            </h1>
                        </div>
                    </div>
                    <div className="px-[3%] pt-2 flex flex-row w-full">
                        <div className="w-[45%]">
                            <Input
                                type="name"
                                placeholder="Иван"
                                title="Имя"
                                value={name}
                                error={errors?.name}
                                setValue={setName}
                            />
                            <Input
                                type="surname"
                                placeholder="Иванов"
                                title="Фамилия"
                                value={surname}
                                error={errors?.surname}
                                setValue={setSurname}
                            />
                            <Input
                                type="patronymic"
                                placeholder="Иванов"
                                title="Отчество"
                                value={patronymic}
                                error={errors?.patronymic}
                                setValue={setPatronymic}
                            />

                            <Input
                                type="email"
                                placeholder="email@example.com"
                                title="Почта"
                                value={email}
                                disabled
                                setValue={setEmail}
                            />
                            <p className="text-lg font-[Montserrat] my-4">
                                ApiKey: {userData?._id}
                            </p>
                            <div
                                onClick={updateUserData}
                                className="px-12 py-4 bg-[#0067E3] rounded-xl text-md cursor-pointer font-[Montserrat] text-white flex justify-center items-center w-fit">
                                Сохранить
                            </div>
                        </div>
                        <div className="w-[45%] ml-[5%]">
                            {/* <Input
                                type="organization"
                                placeholder="ddd"
                                title="Организация"
                                value={}
                                error={}
                                setValue={}
                            /> */}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Profile;