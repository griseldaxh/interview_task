import { Dialog, Transition } from "@headlessui/react";
import { Fragment, useEffect, useState } from "react";
import { toast } from "sonner";

type Review = {
  review_id: number;
  review_title: string;
  review_description: string;
  rating: number;
};

type ProductData = {
  product_id: number;
  product_asin: string;
  product_brand: string;
  reviews: Review[];
};

const ProductDetails = ({
  productData,
}: {
  productData: ProductData | null;
}) => (
  <div className="w-full py-2">
    <div className="flex flex-col space-y-2">
      <div className="flex items-center">
        <label className="font-bold w-20">Brand: </label>
        <span>{productData?.product_brand}</span>
      </div>
      <div className="flex items-center">
        <label className="font-bold w-20">ASIN: </label>
        <span>{productData?.product_asin}</span>
      </div>
    </div>
  </div>
);

const IssuesList = ({ issues }: { issues: string }) => (
  <div className="mt-4">
    <h4 className="font-medium text-lg mb-3">Issues</h4>
    <div className="flex flex-wrap gap-2">
      {issues
        .split(". ")
        .filter((issue) => issue.trim())
        .map((issue, index) => (
          <span
            key={index}
            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800"
          >
            {issue}
          </span>
        ))}
    </div>
  </div>
);

const ReviewsList = ({ reviews }: { reviews: Review[] }) => (
  <div className="mt-4">
    <h4 className="font-medium text-lg mb-3">Customer Reviews</h4>
    <div className="space-y-4 max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
      {reviews.map((review) => (
        <div key={review.review_id} className="border rounded-lg p-3">
          <div className="flex justify-between items-center mb-2">
            <h5 className="font-medium">{review.review_title}</h5>
            <div className="flex items-center">
              <span className="text-yellow-500">
                {"★".repeat(review.rating)}
              </span>
              <span className="text-gray-300">
                {"★".repeat(5 - review.rating)}
              </span>
            </div>
          </div>
          <p className="text-sm text-gray-600">{review.review_description}</p>
        </div>
      ))}
    </div>
  </div>
);

export default function ProductOverview({
  isOpen,
  closeModal,
  title,
  children,
  issues,
  product_id,
  actionButton,
}: {
  isOpen: boolean;
  closeModal: () => void;
  title: string;
  issues: string;
  product_id: number;
  children?: React.ReactNode;
  actionButton?: React.ReactNode;
}) {
  const [productData, setProductData] = useState<ProductData | null>(null);
  useEffect(() => {
    const fetchProductData = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_API}/product/${product_id}`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch product data");
        }
        const data = await response.json();
        setProductData(data);
      } catch (error) {
        toast.error(`Error fetching product data: ${error}.`);
        console.error("Error fetching product data:", error);
      }
    };
    if (product_id) {
      fetchProductData();
    }
  }, [product_id]);

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={closeModal}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/25" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-3xl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <Dialog.Title
                  as="h3"
                  className="font-bold text-center leading-6 text-gray-900 py-5"
                >
                  {title}
                </Dialog.Title>
                {children && <div className="mt-2">{children}</div>}
                <ProductDetails productData={productData} />
                <IssuesList issues={issues} />
                {productData?.reviews && (
                  <ReviewsList reviews={productData.reviews} />
                )}
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}
