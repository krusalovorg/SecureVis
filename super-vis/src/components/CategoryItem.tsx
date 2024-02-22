function CategoryItem({
    text,
    onSelect,
    id,
    select
}: { text: string, onSelect?: any, select?: any, id?: any }) {
    return (
        <div
            onClick={() => {
                if (onSelect) {
                    onSelect(id);
                }
            }}
            className={`relative h-[48px] pl-5 cursor-pointer pr-4 py-2 rounded-xl ${select == id ? "bg-[#0067E3] text-white" : "bg-[#F5FAFD] text-black"} flex flex-row items-center w-full font-[Montserrat]`}>
            {text}
        </div>
    )
}

export default CategoryItem;