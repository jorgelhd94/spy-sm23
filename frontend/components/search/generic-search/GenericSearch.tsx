"use client";
import { SubmitBtn } from "@/components/shared/buttons/SubmitBtn/SubmitBtn";
import { SearchIcon } from "@/components/shared/icons/SearchIcon";
import { Input } from "@nextui-org/react";
import React, { useState } from "react";

type GenericSearchProps = {
  handleSearch: Function;
  loading: boolean;
};

export const GenericSearch: React.FC<GenericSearchProps> = (props) => {
  const handleSearch = (formData: FormData) => {
    props.handleSearch(formData.get("searchText"));
  };

  return (
    <div className="max-w-2xl w-full flex flex-col max-md:items-center">
      <form
        action={handleSearch}
        className="w-full flex max-md:flex-col max-md:px-4 gap-4 items-center"
      >
        <Input
          name="searchText"
          variant="bordered"
          autoFocus
          radius="lg"
          classNames={{
            label: "text-black/50 dark:text-white/90",
            input: [
              "bg-transparent",
              "text-black/90 dark:text-white/90",
              "placeholder:text-default-700/50 dark:placeholder:text-white/60",
            ],
            innerWrapper: "bg-transparent",
          }}
          placeholder="Escribe el nombre del producto..."
          startContent={<SearchIcon color="black" />}
        />

        <SubmitBtn loading={props.loading} />
      </form>
    </div>
  );
};
