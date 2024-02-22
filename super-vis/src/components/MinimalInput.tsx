import React from "react";

const MinimalInput = ({
  onChange,
  value,
  placeholder,
  onSelect,
  id,
  select,
}: {
  onChange: any;
  value: any;
  placeholder: any;
  onSelect?: any;
  select?: any;
  id?: any;
}) => {
  return (
    <div
      onClick={() => {
        if (onSelect) {
          onSelect(id);
        }
      }}
      className={`relative h-[48px] pl-3 pr-4 py-2 rounded-xl ${select == id ? "bg-[#0067E3] text-white" : "bg-[#F5FAFD] text-black"} flex flex-row items-center w-full`}>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={`border-none pl-3 h-full focus:outline-none w-full bg-transparent ${select == id ? "placeholder-text-white" : "placeholder-text-[#C9CBD2]"} font-[Montserrat]`}
        placeholder={placeholder}
      />
    </div>
  );
};

export default MinimalInput;
