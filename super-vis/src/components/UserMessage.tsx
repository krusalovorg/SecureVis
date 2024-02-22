import { UserData, getImage } from "../utils/backend";

function UserMessage({ data, setId, setData }: { data: UserData | any, setId?: any, setData?: any }) {
    const select = data?.select;
    return (
        <>
            <div
                onClick={() => {
                    if (setId) {
                        setId(data?.id || 0)
                    }
                    if (setData) {
                        setData(data);
                    }
                }}
                className={`w-full p-5 rounded-3xl flex flex-row items-start mb-2 ${select ? 'bg-[#0067E3]' : ''} cursor-pointer min-w-[410px]`}>
                <img
                    src={getImage(data?.avatar)}
                    className={`min-w-[56px] w-[56px] h-[56px] rounded-full ${select && 'border-white border-2'}`}
                />
                <div className="pl-4" style={{
                    width: "calc(100% - 60px)"
                }}>
                    <div className="w-full flex flex-row items-end">
                        <h1 className={`text-xl ${select ? "text-white" : "text-black"} font-[Montserrat]`}>
                            {data?.surname} {data?.name}
                        </h1>
                        <h2 className={`${select ? "text-white" : "text-black"} ml-auto font-[Montserrat]`}>{data?.date}</h2>
                        {data?.new_message && !select &&
                            <div className={`text-md bg-[#0067E3] w-[28px] h-[28px] rounded-full ml-3 flex font-[Montserrat] justify-center items-center text-white`}>
                                {data?.new_message}
                            </div>}
                    </div>
                    {data?.text ?
                        <h2 className={`text-lg ${select ? "text-white" : "text-black"} font-[Montserrat] four_text mt-2 h-[25px]`}>
                            {data?.text}
                        </h2>
                        :
                        <h1 className={`text-lg ${select ? "text-white" : "text-black"} font-[Montserrat]`}>
                            {data?.position}
                        </h1>
                    }
                </div>
            </div>
        </>
    )
}

export default UserMessage;