function Input({
    placeholder,
    setValue,
    value,
    title,
    type,
    disabled,
    error
}: {
    placeholder: string,
    setValue: any,
    value: string,
    title: string,
    type?: string,
    disabled?: boolean,
    error?: string
}) {
    return (
        <>
            {title && <h2 className="text-md text-black font-[Montserrat] mb-2 pl-5">{title}</h2>}
            <div className={`w-full px-6 bg-white h-[70px] shadow-md rounded-xl flex flex-row items-center ${error ? "border-red-500 border-2 ring-red-500" : "mb-5"}`}>
                <input
                    type={type || "text"}
                    disabled={disabled}
                    className="border-none h-full focus:outline-none w-full bg-transparent placeholder-text-[#C9CBD2] font-[Montserrat]"
                    placeholder={placeholder}
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                />
            </div>
            {error &&
                <h2 className="text-md text-red-500 font-[Montserrat] mb-5 mt-2">{error}</h2>
            }
        </>
    )
}

export default Input;