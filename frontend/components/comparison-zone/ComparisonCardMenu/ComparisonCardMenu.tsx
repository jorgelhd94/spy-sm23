"use client";
import { VerticalDots } from "@/components/shared/icons/VerticalDots";
import { DeleteModal } from "@/components/shared/modals/DeleteModal";
import {
  Button,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
} from "@nextui-org/react";
import { revalidatePath } from "next/cache";
import { useRouter } from "next/navigation";
import React, { useState } from "react";
import { toast } from "react-toastify";
import { useSWRConfig } from "swr";

type ComparisonCardMenuProps = {
  comparisonZoneId: string | number;
};

export const ComparisonCardMenu: React.FC<ComparisonCardMenuProps> = (
  props
) => {
  const [openDeleteModal, setOpenDeleteModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { mutate } = useSWRConfig();

  const router = useRouter();

  const handleDelete = async () => {
    setIsLoading(true);

    await fetch(
      `${process.env.NEXT_PUBLIC_API_URL!}api/v1/comparison_zones/${
        props.comparisonZoneId
      }/`,
      {
        method: "DELETE",
      }
    )
      .then(() => {
        toast.success("Zona eliminada correctamente");
        setOpenDeleteModal(false);
        mutate(`${process.env.NEXT_PUBLIC_API_URL!}api/v1/comparison_zones/`);
      })
      .catch(() => {
        toast.error("Ha ocurrido un error al eliminar la Zona");
      });

    setIsLoading(false);
  };

  return (
    <>
      <Dropdown>
        <DropdownTrigger>
          <Button
            isIconOnly
            className="z-20 bg-white"
            radius="lg"
            color="default"
            variant="bordered"
          >
            <VerticalDots />
          </Button>
        </DropdownTrigger>
        <DropdownMenu aria-label="Static Actions">
          <DropdownItem
            key="delete"
            description="Eliminar zona de comparación"
            color="danger"
            onPress={() => setOpenDeleteModal(true)}
          >
            Eliminar
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>

      <DeleteModal
        isOpen={openDeleteModal}
        handleDelete={handleDelete}
        onOpenChange={setOpenDeleteModal}
        isLoading={isLoading}
      />
    </>
  );
};
