import { Select, SelectItem } from "@nextui-org/react";
import React, { useEffect, useState } from "react";

type OrderByProps = {
  handleOrderBy: Function;
  isDisabled?: boolean;
  orderByOption: number;
};

export const OrderBy: React.FC<OrderByProps> = ({
  handleOrderBy,
  isDisabled,
  orderByOption,
}) => {
  const options = [
    { value: "-1", text: "Sin ordenar" },
    { value: "0", text: "Menor precio" },
    { value: "1", text: "Mayor precio" },
    { value: "2", text: "Más nuevo" },
    { value: "3", text: "Menor precio/lb" },
  ];

  const [defaultOption, setDefaultOption] = useState(["-1"]);

  useEffect(() => {
    setDefaultOption([orderByOption.toString()]);
  }, [orderByOption]);

  return (
    <Select
      isDisabled={isDisabled}
      selectedKeys={defaultOption}
      selectionMode="single"
      variant="faded"
      label="Ordenar por"
      className="max-w-64"
      onChange={(event) => handleOrderBy(event.target.value)}
    >
      {options.map((option) => (
        <SelectItem key={option.value} value={option.value}>
          {option.text}
        </SelectItem>
      ))}
    </Select>
  );
};
