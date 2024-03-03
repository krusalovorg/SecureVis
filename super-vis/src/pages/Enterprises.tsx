import { useContext, useEffect, useRef, useState } from "react";
import { Enterprise, URL_SERVER, getCookieToken, getEnterprises, getImage } from "../utils/backend";
import Input from "../components/Input";
import UserContext from "../contexts/UserContext";
import { Card, Typography } from "@material-tailwind/react";

const TABLE_HEAD = [
    "Название", "Почта", "id", "Действие"
]

function Enterprises() {
    const [enterprisesList, setEnterprisesList] = useState<Enterprise[]>([]);
    const userData = useContext(UserContext);
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [patronymic, setPatronymic] = useState('');

    const [email, setEmail] = useState('');
    const [result, setResult] = useState('');

    const [edit, setEdit] = useState(false);
    const [id, setId] = useState<null | string>(null);

    const [errors, setErrors] = useState({
        name: '',
        email: '',
        password: '',
    });

    const checkErrors = () => {
        const fields = { name, email, ...(edit ? {} : {password}) };
        let error = false;
        let errors_res = errors;
        for (const field in fields) {
            const value = (fields as any)[field];
            if (value?.length === 0) {
                errors_res = { ...errors_res, [field]: "Поле не заполнено" }
                error = true;
            } else {
                errors_res = { ...errors_res, [field]: "" }
            }
        }
        setErrors(errors_res)
        return error;
    };

    async function loadEnterprises() {
        const result = await getEnterprises();
        if (result) {
            setEnterprisesList(result as Enterprise[]);
        }
    }

    async function addOrg() {
        const errors = checkErrors();
        if (!errors) {
            fetch(URL_SERVER + '/enterprise', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + getCookieToken(),
                },
                body: JSON.stringify({
                    email, name, password
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log('User add successfully:', data);
                    setResult(data?.message)
                })
                .catch(error => {
                    console.error('Error add user:', error);
                });
        }
    }


    async function editOrg() {
        const errors = checkErrors();
        if (!errors) {
            fetch(URL_SERVER + '/enterprise', {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + getCookieToken(),
                },
                body: JSON.stringify({
                    email, name, ...(password ? {password} : {}), id
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log('User add successfully:', data);
                    setResult(data?.message)
                    document.location.reload()
                })
                .catch(error => {
                    console.error('Error add user:', error);
                });
        }
    }


    useEffect(() => {
        loadEnterprises()
    }, [])

    return (
        <div className="w-full h-full flex justify-center align-center">
            <div className="w-full pb-[100px] h-fit">
                <div style={{height: 68}}></div>
                <div className="w-[90%] h-fit bg-[#F5FAFD] rounded-3xl relative m-auto">
                    <div className="w-full bg-white h-[80px] rounded-t-3xl flex flex-row items-center px-5 mb-5">
                        <div className="ml-5 gap-2">
                            <h1 className={`text-xl text-black font-[Montserrat]`}>
                                Организации
                            </h1>
                        </div>
                    </div>
                    <div className="px-[3%] pt-2 flex flex-col w-full">
                        <Input
                            type="name"
                            placeholder="Оргаизация"
                            title="Название организации"
                            value={name}
                            error={errors?.name}
                            setValue={setName}
                        />
                        <Input
                            type="email"
                            placeholder="email@example.com"
                            title="Почта"
                            value={email}
                            setValue={setEmail}
                        />
                        <Input
                            type="patronymic"
                            placeholder="..."
                            title="Пароль"
                            value={password}
                            error={errors?.password}
                            setValue={setPassword}
                        />
                        <div
                            onClick={edit ? editOrg : addOrg}
                            className="px-12 py-4 bg-[#0067E3] rounded-xl text-md cursor-pointer font-[Montserrat] text-white flex justify-center items-center w-fit">
                            {edit ? "Сохранить" : "Добавить"}
                        </div>
                        <a>
                            {result}
                        </a>
                        <table className="w-full mt-5 min-w-max table-auto text-left rounded-lg">
                            <thead>
                                <tr>
                                    {TABLE_HEAD.map((head) => (
                                        <th
                                            key={head}
                                            className="font-medium border-b bg-white p-4"
                                        >
                                            {head}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {enterprisesList && enterprisesList.length > 0 &&
                                    enterprisesList.map(({ name, email, _id }, index) => {
                                        const isLast = index === enterprisesList.length - 1;
                                        const classes = isLast ? "p-4" : "p-4 border-b border-blue-gray-50";

                                        return (
                                            <tr key={name}>
                                                <td className={classes}>
                                                    {name}
                                                </td>
                                                <td className={classes}>
                                                    {email}
                                                </td>
                                                <td className={classes}>
                                                    {_id}
                                                </td>
                                                <td className={classes}>
                                                    <div
                                                        onClick={() => {
                                                            setEmail(email)
                                                            setName(name)
                                                            setEdit(true)
                                                            setId(_id)
                                                        }}
                                                        className="px-8 py-2 bg-[#0067E3] rounded-xl text-md cursor-pointer font-[Montserrat] text-white flex justify-center items-center w-fit">
                                                        Изменить
                                                    </div>
                                                </td>
                                            </tr>
                                        );
                                    })}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Enterprises;