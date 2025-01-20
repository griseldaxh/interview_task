import { TableColumns } from "./TableColumns";

interface Product {
  product_id: string;
  asin: string;
  brand: string;
  review_count: number;
  positive_percentage: number;
  negative_percentage: number;
  top_issues: string;
}

interface ProductTableProps {
  products: Product[] | null;
  onProductSelect: (product: Product) => void;
}

export function ProductTable({ products, onProductSelect }: ProductTableProps) {
  return (
    <table className="min-w-full divide-y divide-gray-200">
      <thead className="bg-gray-50">
        <tr>
          {TableColumns.map((column) => (
            <th
              key={column.name}
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              {column.name}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className="bg-white divide-y divide-gray-200">
        {products?.map((product) => (
          <tr
            key={product.product_id}
            className="hover:bg-gray-50 cursor-pointer"
            onClick={() => onProductSelect(product)}
          >
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {product.product_id}
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
              {product.brand}
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
              {product.asin}
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
              {product.review_count}
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
              {product.positive_percentage}
            </td>
            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
              {product.negative_percentage}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
