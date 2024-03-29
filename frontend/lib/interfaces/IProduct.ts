import { IManufacture } from "./IManufacture";

export interface IProduct {
  id: string;
  name: string;
  product_url: string;
  image_url: string;
  manufacture: IManufacture;
  current_price: number;
  currency: string;
  price_by_weight: {
    price: number;
    currency: string;
  } | null;
}
