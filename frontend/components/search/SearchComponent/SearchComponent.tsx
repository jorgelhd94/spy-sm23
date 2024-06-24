"use client";

import { ProductCard } from "@/components/products/ProductCard/ProductCard";
import { ErrorMsg } from "@/components/shared/messages/ErrorMsg/ErrorMsg";
import { HidePinProductContext } from "@/lib/context/HidePinProductContext";
import { PinProductContext } from "@/lib/context/PinProductContext";
import { ISearchProducts } from "@/lib/interfaces/ISearchProducts";
import { getApiUrl } from "@/lib/utils/api/api";
import { useSearchParams } from "next/navigation";
import React, { useCallback, useContext, useEffect, useState } from "react";
import ProductSearchGrid from "../../products/ProductSearchGrid/ProductSearchGrid";
import { SearchForm } from "../SearchForm/SearchForm";

type Props = {
  hideSaveSearch?: boolean;
};

export const SearchComponent: React.FC<Props> = (props) => {
  const { pinProduct, setPinProduct } = useContext(PinProductContext);
  const hidePinProduct = useContext(HidePinProductContext);
  const searchParams = useSearchParams();

  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const [searchResults, setSearchResults] = useState<ISearchProducts | null>(
    null
  );

  const handleSearchProducts = useCallback(async () => {
    setLoading(true);
    setIsError(false);

    try {
      const response = await fetch(
        `${getApiUrl()}/search/?${searchParams.toString()}`
      );
      if (response.status !== 200) {
        throw new Error("Error fetching data");
      }
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      setIsError(true);
    } finally {
      setLoading(false);
    }
  }, [searchParams]);

  useEffect(() => {
    handleSearchProducts();
  }, [searchParams.toString()]);

  return (
    <div className="flex flex-col items-center gap-8 max-md:pt-4 w-full">
      <div className="flex max-md:flex-col items-center gap-2 max-w-3xl w-full">
        <SearchForm
          loading={loading}
          hideSaveSearch={props.hideSaveSearch}
          handleSearchText={handleSearchProducts}
        />
      </div>

      <div className="flex max-md:flex-col justify-between px-4 gap-4 w-full">
        {pinProduct && !hidePinProduct && (
          <div className="h-max sticky top-16 lg:top-20 z-30 flex md:flex-col justify-center">
            <h3 className="text-xl font-medium pb-4 max-md:hidden">
              Producto fijado
            </h3>
            <ProductCard product={pinProduct} />
          </div>
        )}

        <div className="flex justify-center w-full">
          {isError ? (
            <ErrorMsg />
          ) : (
            <ProductSearchGrid
              searchResults={searchResults}
              loading={loading}
            />
          )}
        </div>
      </div>
    </div>
  );
};
