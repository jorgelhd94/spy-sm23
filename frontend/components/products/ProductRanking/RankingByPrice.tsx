"use client";
import { Chip } from "@nextui-org/react";
import React, { useState } from "react";

type Props = {};

const RankingByPrice = (props: Props) => {
  const [rankingByPrice, setRankingByPrice] = useState(0);
  return (
    <div className="flex gap-2 items-center">
      <p className="text-sm font-bold">Top - precio:</p>
      <Chip>{rankingByPrice} de {rankingByPrice}</Chip>
    </div>
  );
};

export default RankingByPrice;
