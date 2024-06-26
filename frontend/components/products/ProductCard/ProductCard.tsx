import { PinBtn } from "@/components/shared/buttons/PinBtn/PinBtn";
import { PinProductContext } from "@/lib/context/PinProductContext";
import { IProduct } from "@/lib/interfaces/IProduct";
import {
  getArrowByWeightStyle,
  getArrowIcon,
  getPriceByWeightStyle,
  getPriceStyle,
} from "@/lib/utils/functions/pricesStyle";
import { Card, CardBody, Image } from "@nextui-org/react";
import React, { useContext, useEffect, useState } from "react";
import { ProductDropdownMenu } from "../ProductDropdownMenu/ProductDropdownMenu";

type ProductCardProps = {
  product: IProduct;
  hideSetPin?: boolean;
  hideMenu?: boolean;
};

export const ProductCard: React.FC<ProductCardProps> = (props) => {
  const { pinProduct, setPinProduct } = useContext(PinProductContext);

  const [isPinActive, setIsPinActive] = useState(
    pinProduct?.product_id === props.product.product_id
  );

  const handlePinProduct = (isActive: boolean) => {
    setIsPinActive(isActive);

    if (!setPinProduct) {
      return;
    }

    if (isActive) {
      setPinProduct(props.product);
    } else {
      setPinProduct(null);
    }
  };

  useEffect(() => {
    if (pinProduct?.product_id !== props.product.product_id) {
      setIsPinActive(false);
    }
  }, [pinProduct?.product_id, props.product.product_id]);

  return (
    <>
      <Card shadow="sm" className="w-full sm:w-72 md:w-64">
        <CardBody className="overflow-visible p-0">
          <div className="grid grid-cols-12">
            <div className="relative col-span-6 md:col-span-12 max-md:my-2 max-md:ml-2">
              <Image
                radius="lg"
                width="100%"
                alt={props.product.name}
                className="w-full object-cover h-[140px] md:h-[240px]"
                src={props.product.image_url}
              />

              {!props.hideSetPin && (
                <div className="absolute top-1 left-1">
                  <PinBtn
                    isActive={isPinActive}
                    handleClick={handlePinProduct}
                  />
                </div>
              )}

              {!props.hideMenu && (
                <div className="absolute top-1 right-1">
                  <ProductDropdownMenu product={props.product} />
                </div>
              )}
            </div>

            <div className="col-span-6 md:col-span-12 flex flex-col items-start text-start justify-start gap-2 p-4">
              <a
                href={props.product.product_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                <b className="text-small text-primary-800">
                  {props.product.name}
                </b>
              </a>

              <a
                href={props.product.manufacture.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                <p className="text-small font-medium">
                  Marca: {props.product.manufacture.name}
                </p>
              </a>

              <div>
                <p
                  className={`font-bold text-lg flex items-center gap-1 ${getPriceStyle(
                    pinProduct,
                    props.product
                  )}`}
                >
                  {props.product.current_price} {props.product.currency}
                  <span>{getArrowIcon(pinProduct, props.product)}</span>
                </p>

                {props.product.price_by_weight && (
                  <p
                    className={`font-bold text-sm flex items-center ${getPriceByWeightStyle(
                      pinProduct,
                      props.product
                    )}`}
                  >
                    {props.product.price_by_weight}{" "}
                    {props.product.currency_by_weight}
                    <span>
                      {getArrowByWeightStyle(pinProduct, props.product)}
                    </span>
                  </p>
                )}
              </div>
            </div>
          </div>
        </CardBody>
      </Card>
    </>
  );
};
