import { useContext, useEffect, useRef, useState } from "react";
import { Enterprise, URL_SERVER, getCookieToken, getEnterprises, Staff, getStaffs } from "../utils/backend";
import Input from "../components/Input";
import UserContext from "../contexts/UserContext";
import { Card, Typography } from "@material-tailwind/react";

const TABLE_HEAD = [
    "ФИО", "Должность", "Время работы (День)", "Начал работу", "Закончил работу", "Камера", "id"
]

function LogsPage() {
    const [staffList, setStaffList] = useState<Staff[]>([]);
    const [logs, setLogs] = useState<any[]>([]);
    const userData = useContext(UserContext);

    async function loadStaffs() {
        if (userData?._id) {
            const result = await getStaffs(userData?._id);
            if (result) {
                setStaffList(result as Staff[]);

                const allLogs = result.flatMap(staff =>
                    staff.statistics.flatMap(stat =>
                        stat.logs.map((log: any) => ({
                            ...log,
                            name: staff.name,
                            _id: staff._id,
                            position: staff.position,
                            day: stat?.day,
                            total_work_time: stat?.total_work_time
                        }))
                    )
                );
                // Теперь sortedLogs содержит все логи, отсортированные по time_start

                const result1 = allLogs.sort((a, b) => {
                    // Добавление произвольной даты к времени для создания объекта Date
                    let aDateStart = new Date('1970-01-01T' + a.time_start + 'Z');
                    let bDateStart = new Date('1970-01-01T' + b.time_start + 'Z');

                    // Сравнение дат
                    if (aDateStart < bDateStart) {
                        return 1;
                    } else if (aDateStart > bDateStart) {
                        return -1;
                    } else {
                        return 0;
                    }
                });
                console.log(result1);
                setLogs(result1)
            }
        }
    }

    useEffect(() => {
        loadStaffs()
    }, [userData])

    return (
        <div className="w-full h-full flex justify-center align-center">
            <div className="w-full pb-[100px] h-fit">
                <div style={{ height: 68 }}></div>
                <div className="w-[90%] pb-[55px] h-fit bg-[#F5FAFD] rounded-3xl relative m-auto">
                    <div className="w-full bg-white h-[80px] rounded-t-3xl flex flex-row items-center px-5 mb-5">
                        <div className="ml-5 gap-2">
                            <h1 className={`text-xl text-black font-[Montserrat]`}>
                                Общие логи системы
                            </h1>
                        </div>
                    </div>
                    <div className="px-[3%] pt-2 flex flex-col w-full">
                        {logs && logs?.length > 0 &&
                            logs?.map((item, index) => {
                                const isLast = index === logs.length - 1;
                                const classes = isLast ? "p-4" : "p-4 border-b border-blue-gray-50";

                                let dateStart = new Date('1970-01-01T' + item.time_start + 'Z');
                                let dateEnd = new Date('1970-01-01T' + item.time_end + 'Z');
                                let diff = dateEnd.getTime() - dateStart.getTime();
                                diff = Math.floor(diff / 1000 / 60);

                                return (
                                    <div key={index}>
                                        {item.time_end ?
                                            <>
                                                {`${item.time_end}: ${item.name} Вышел. Проработал: ${diff}~ минут. ${item.name} ${item._id}`}
                                                <img className="inline-flex ml-2 ronded-base" src={URL_SERVER + "/image/" + item?.end_photo_path} />
                                            </>
                                            : ''}
                                        <br />
                                        {item.time_start}: {item.name} вошел ID: {item._id}
                                        <img className="inline-flex ml-2 ronded-base" src={URL_SERVER + "/image/" + item?.start_photo_path} />
                                    </div>
                                );
                            })}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default LogsPage;