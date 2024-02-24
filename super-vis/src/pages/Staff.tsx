import { useContext, useEffect, useRef, useState } from "react";
import { Enterprise, URL_SERVER, getCookieToken, getEnterprises, Staff, getStaffs } from "../utils/backend";
import Input from "../components/Input";
import UserContext from "../contexts/UserContext";
import { Card, Typography } from "@material-tailwind/react";

const TABLE_HEAD = [
    "ФИО", "Должность", "id", "Действие"
]

const days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Вс", "Сб"]

function StaffPage() {
    const [staffList, setStaffList] = useState<Staff[]>([]);
    const userData = useContext(UserContext);
    const [name, setName] = useState('');
    const [position, setPosition] = useState('');

    const [result, setResult] = useState('');
    const [isHovered, setIsHovered] = useState(false);

    const [file, setFile] = useState<any>();
    const [newFileAsImage, setNewFileAsImage] = useState<any>();

    const [timetable, setTimetable] = useState<string[]>([]);

    const [startTime, setStartTime] = useState("08:30");
    const [endTime, setEndTime] = useState("18:00");

    const [errors, setErrors] = useState({
        name: '',
        email: '',
        position: '',
    });

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files: any = e.target.files;
        setFile(files[0]);

        const reader = new FileReader();
        reader.onload = (event) => {
            if (event.target) {
                const result = event.target.result as ArrayBuffer;
                // преобразование массива байт в изображение
                const blob = new Blob([result], { type: "image/" });
                const urlCreator = window.URL || window.webkitURL;
                const imageUrl = urlCreator.createObjectURL(blob);
                setNewFileAsImage(imageUrl);
            }
        };
        if (files[0]) {
            reader.readAsArrayBuffer(files[0]);
        }
    };

    const checkErrors = () => {
        const fields = { name, position };
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

    async function loadStaffs() {
        console.log('userData?._id ', userData?._id)
        if (userData?._id) {
            const result = await getStaffs(userData?._id);
            if (result) {
                setStaffList(result as Staff[]);
            }
        }
    }

    async function addOrg() {
        const errors = checkErrors();
        if (!errors) {
            const fields = { name, position, startTime, endTime };
            const new_userData = new FormData();
            for (const field in fields) {
                const value = (fields as any)[field];
                console.log(value, (userData as any)[field], field)
                if (value != (userData as any)[field] && value.length > 0) {
                    new_userData.append(field, value);
                }
            }

            new_userData.append('timetable', JSON.stringify(timetable))

            if (file) {
                new_userData.append('face', file, file.name);
            }

            fetch(URL_SERVER + '/staff', {
                method: 'POST',
                headers: {
                    Authorization: "Bearer " + getCookieToken(),
                },
                body: new_userData
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
        loadStaffs()
    }, [userData])

    return (
        <div className="w-full h-full flex justify-center align-center">
            <div className="w-full h-full flex justify-center items-center">
                <div className="w-[90%] h-[90%] bg-[#F5FAFD] rounded-3xl relative">
                    <div className="w-full bg-white h-[80px] rounded-t-3xl flex flex-row items-center px-5 mb-5">
                        <div className="ml-5 gap-2">
                            <h1 className={`text-xl text-black font-[Montserrat]`}>
                                Сотрудники
                            </h1>
                        </div>
                    </div>
                    <div className="px-[3%] pt-2 flex flex-col w-full">
                        <Input
                            type="name"
                            placeholder="Оргаизация"
                            title="ФИО сотрудника"
                            value={name}
                            error={errors?.name}
                            setValue={setName}
                        />
                        <Input
                            type="patronymic"
                            placeholder="Программист"
                            title="Должность"
                            value={position}
                            error={errors?.position}
                            setValue={setPosition}
                        />
                        <div className="flex flex-row mb-4">
                            <div className="flex flex-col">
                                <p className="mb-2 text-md font-[Montserrat]">Начало</p>
                                <input
                                    onChange={(e) => {
                                        setStartTime(e.target.value)
                                    }}
                                    value={startTime}
                                    className="w-fit px-6 bg-white h-[70px] shadow-md rounded-xl flex flex-row justify-center items-center" type={"time"} />
                            </div>
                            <div className="flex flex-col ml-4">
                                <p className="mb-2 text-md font-[Montserrat]">Конец</p>
                                <input
                                onChange={(e)=>{
                                    setEndTime(e.target.value)
                                }}
                                value={endTime}
                                className="w-fit px-6 bg-white h-[70px] shadow-md rounded-xl flex flex-row justify-center items-center" type={"time"} />
                            </div>
                        </div>
                        <p className="text-md text-black font-[Montserrat]">Рабочие дни:</p>
                        <div className="flex flex-row gap-2 mb-3 mt-2">
                            {days && days.map((day, index) => {
                                return (
                                    <div
                                        onClick={() => {
                                            if (timetable.includes(day)) {
                                                setTimetable(timetable.filter(item => item !== day));
                                            } else {
                                                setTimetable([...timetable, day])
                                            }
                                        }}
                                        className={
                                            `px-3 py-2 cursor-pointer ${timetable.includes(day) ? "bg-[#0067E3] text-white" : "bg-gray-100"}  rounded-lg`
                                        }
                                        key={index}>
                                        {day}
                                    </div>
                                )
                            })}
                        </div>
                        <div
                            className="bg-white shadow-md w-fit p-5 rounded-xl mb-5 flex flex-col justify-center items-center cursor-pointer relative"
                            onMouseEnter={() => setIsHovered(true)}
                            onMouseLeave={() => setIsHovered(false)}
                        >
                            {isHovered && (
                                <div className="absolute top-0 bg-gray-800 bg-opacity-25 rounded-xl w-full h-full flex items-center justify-center">
                                    <div className="text-white text-lg">Добавить изображение</div>
                                    <input
                                        className="absolute w-full h-full opacity-0"
                                        type="file"
                                        accept=".jpg,.png"
                                        onChange={handleImageChange}
                                    />
                                </div>
                            )}
                            <img
                                src={newFileAsImage}
                                className={`min-w-[160px] h-[160px] rounded-md`}
                                style={{
                                    aspectRatio: 1
                                }}
                            />
                            <h2 className="text-sm text-black font-[Montserrat] mt-2 truncate max-w-[200px]">{file ? file?.name : "Наведите чтобы изменить"}</h2>
                        </div>

                        <div
                            onClick={addOrg}
                            className="px-12 py-4 bg-[#0067E3] rounded-xl text-md cursor-pointer font-[Montserrat] text-white flex justify-center items-center w-fit">
                            Добавить
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
                                {staffList && staffList.length > 0 &&
                                    staffList.map(({ name, position, _id }, index) => {
                                        const isLast = index === staffList.length - 1;
                                        const classes = isLast ? "p-4" : "p-4 border-b border-blue-gray-50";

                                        return (
                                            <tr key={name}>
                                                <td className={classes}>
                                                    {name}
                                                </td>
                                                <td className={classes}>
                                                    {position}
                                                </td>
                                                <td className={classes}>
                                                    {_id}
                                                </td>
                                                <td className={classes}>
                                                    <div
                                                        onClick={() => {
                                                            setName(name)
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

export default StaffPage;