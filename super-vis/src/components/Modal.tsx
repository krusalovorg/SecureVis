function Modal({ open, setOpen, children, title }: { open: boolean, setOpen: any, title: string, children: any }) {

    if (!open) {
        return <></>
    }

    return (
        <>
            <div className="w-full h-full fixed left-0 top-0 z-[100]">
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl p-5 z-[101] w-fit">
                    <div className="w-full h-[60px] flex flex-row justify-between items-center min-w-[500px]">
                        <h1 className={`text-xl text-black font-bold font-[Montserrat]`}>
                            {title}
                        </h1>
                        <svg onClick={()=>setOpen(false)} className="cursor-pointer" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M20 4L4 20M20 20L4 4" stroke="black" stroke-width="2" stroke-linecap="round" />
                        </svg>
                    </div>
                    {children}
                </div>
                <div className="absolute w-full h-full z-[100] bg-black opacity-40" />
            </div>
        </>
    )
}

export default Modal;