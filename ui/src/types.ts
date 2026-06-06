export type ProductStatus = 'ENOUGH' | 'REQUIRED' | 'EMERGENCY';

export interface ProductCategory {
  id: string;
  name: string;
}

export interface Product {
  id: string;
  name: string;
  category_id: string;
  category?: ProductCategory;
}

export interface User {
  id: string;
  name: string;
  role: string;
}

export interface ProductState {
  product: Product;
  bar: User;
  status: ProductStatus;
}
