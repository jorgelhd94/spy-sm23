import React from "react";

type SearchIconProps = {
  isBlack?: boolean;
};

export const SearchIcon: React.FC<SearchIconProps> = ({ isBlack = false }) => {
  const getColor = () => {
    if (isBlack)
      return "text-black/75 hover:text-black/90 mb-0.5 dark:text-white/90";
    return "text-white hover:text-white/80 mb-0.5";
  };
  
  return (
    <svg
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
      width="1.4em"
      className={"w-6 h-6 pointer-events-none " + getColor()}
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
      ></path>
    </svg>
  );
};
