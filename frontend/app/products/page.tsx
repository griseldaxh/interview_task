"use client";

import { Suspense } from "react";
import dynamic from "next/dynamic";

import ProductsSection from "@/components/pages/products/ProductsSection";
import QueryProvider from "@/providers/QueryProvider";

const Spinner = dynamic(() => import("@/components/ui/Spinner"), {
  ssr: false,
  loading: () => <div className="w-[240px] h-[240px]" />,
});

export default function PotentialPage() {
  return (
    <div className="w-full max-w-[1200px]">
      <QueryProvider>
        <Suspense fallback={<Spinner />}>
          <ProductsSection />
        </Suspense>
      </QueryProvider>
    </div>
  );
}
