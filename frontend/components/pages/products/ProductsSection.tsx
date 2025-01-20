"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

import Spinner from "@/components/ui/Spinner";
import { ANIMATION_CONFIG } from "@/lib/constants";
import { toast } from "@/components/ui/toaster";

import ProductOverview from "./ProductOverview";
import { ProductTable } from "./ProductTable";
import { TablePagination } from "./TablePagination";

interface Product {
  product_id: string;
  asin: string;
  brand: string;
  review_count: number;
  positive_percentage: number;
  negative_percentage: number;
  top_issues: string;
}

export default function ProductsSection() {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [selectedProduct, setSelectedProduct] = useState<number>(0);
  const [page, setPage] = useState<number>(0);
  const [issues, setIssues] = useState<string>("");
  const [pageSize, setPageSize] = useState<number>(10);
  const [total, setTotal] = useState<number>(0);
  const [products, setProducts] = useState<Product[] | null>(null);

  const handleProductSelect = (product: Product) => {
    setIssues(product.top_issues);
    setSelectedProduct(Number(product.product_id));
    setIsOpen(true);
  };

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setIsLoading(true);

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_API}/products?page=${
            page + 1
          }&page_size=${pageSize}`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch product data");
        }
        const data = await response.json();
        setTotal(data.total);
        setProducts(data.products);
        setIsLoading(false);
      } catch (error) {
        toast.error(`Error fetching product data: ${error}.`);
        console.error("Error fetching product data:", error);
      }
    };

    fetchProducts();
  }, [page, pageSize]);

  if (isLoading) {
    return (
      <div className="flex w-full justify-center">
        <Spinner />
      </div>
    );
  }

  return (
    <motion.div
      className="flex w-full flex-col gap-4 p-4 mt-24"
      variants={ANIMATION_CONFIG.container}
      initial="hidden"
      animate="show"
    >
      <h1 className="text-center text-4xl font-bold text-gray-900 py-4">
        Products Overview
      </h1>

      <ProductOverview
        isOpen={isOpen}
        product_id={selectedProduct}
        issues={issues}
        closeModal={() => setIsOpen(false)}
        title="Product Overview"
      />

      <div className="overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
        <ProductTable
          products={products}
          onProductSelect={handleProductSelect}
        />
        <TablePagination
          currentPage={page}
          onPageChange={setPage}
          totalPages={Math.ceil(total / pageSize)}
        />
      </div>
    </motion.div>
  );
}
