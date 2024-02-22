import React from 'react';

const SearchInput = ({onChange}: {onChange: any}) => {
  return (
    <div className="relative h-[48px] pl-3 pr-4 py-2 rounded-xl bg-[#F5FAFD] flex flex-row items-center w-full">
      <div className="pointer-events-none">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 text-[#C9CBD2]"
        >
          <path
            d="M16.927 17.0401L20.4001 20.4001M19.2801 11.4401C19.2801 15.77 15.77 19.2801 11.4401 19.2801C7.11019 19.2801 3.6001 15.77 3.6001 11.4401C3.6001 7.11019 7.11019 3.6001 11.4401 3.6001C15.77 3.6001 19.2801 7.11019 19.2801 11.4401Z"
            stroke="#C9CBD2"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
      </div>
      <input
        type="text"
        onChange={(e)=>onChange(e.target.value)}
        className="border-none pl-3 h-full focus:outline-none w-full bg-transparent placeholder-text-[#C9CBD2] font-[Montserrat]"
        placeholder='Найти'
      />
    </div>
  );
};

export default SearchInput;