"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/Button";

export default function MainSection() {
  const router = useRouter();

  return (
    <div className="bg-black px-6 py-8 text-white md:py-16">
      <div className="mx-auto max-w-4xl">
        <h1 className="mb-6 text-center font-normal leading-tight">
          <span className="font-semibold">Supercharge </span>
          Your Sales Team with
          <span className="font-semibold">AI</span>
        </h1>
        <p className="mx-auto mb-8 max-w-2xl text-center text-lg font-light md:text-xl">
          Effortlessly Monitor Product Performance{" "}
          <span className="font-medium">with</span> SellerX.
          <br className="hidden sm:block" />
          Streamline Your Brand Management{" "}
          <span className="font-medium">Across Amazon Marketplaces.</span>
        </p>
        <div className="w-full flex justify-center">
          <div className="flex items-center justify-between rounded-full p-2 shadow-[0_0_15px_2px_rgba(255,92,53,0.9)]">
            <Button
              variant="secondary"
              className={`items-center justify-center ${"font-base whitespace-nowrap flex py-6"}`}
              onClick={() => router.push("/products")}
            >
              <span className="">Unlock Organic Revenue</span>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
