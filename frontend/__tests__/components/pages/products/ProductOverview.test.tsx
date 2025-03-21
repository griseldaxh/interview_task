import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ProductOverview from "@/components/pages/products/ProductOverview";
import { toast } from "sonner";

// Mock the toast
jest.mock("sonner", () => ({
  toast: {
    error: jest.fn(),
  },
}));

// Mock fetch
global.fetch = jest.fn();

describe("ProductOverview", () => {
  const mockProps = {
    isOpen: true,
    closeModal: jest.fn(),
    title: "Test Product",
    issues: "Issue 1. Issue 2. Issue 3",
    product_id: 123,
  };

  const mockProductData = {
    product_id: 123,
    product_asin: "B00TEST123",
    product_brand: "Test Brand",
    reviews: [
      {
        review_id: 1,
        review_title: "Great product",
        review_description: "Really enjoyed using this",
        rating: 5,
      },
      {
        review_id: 2,
        review_title: "Good but could be better",
        review_description: "Decent product overall",
        rating: 4,
      },
    ],
  };

  beforeEach(() => {
    jest.clearAllMocks();
    (global.fetch as jest.Mock).mockReset();
  });

  it("renders the component with basic props", () => {
    render(<ProductOverview {...mockProps} />);
    expect(screen.getByText(mockProps.title)).toBeInTheDocument();
  });

  it("displays issues correctly", () => {
    render(<ProductOverview {...mockProps} />);
    expect(screen.getByText("Issue 1")).toBeInTheDocument();
    expect(screen.getByText("Issue 2")).toBeInTheDocument();
    expect(screen.getByText("Issue 3")).toBeInTheDocument();
  });

  it("fetches and displays product data successfully", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockProductData,
    });

    render(<ProductOverview {...mockProps} />);

    await waitFor(() => {
      expect(
        screen.getByText(mockProductData.product_brand)
      ).toBeInTheDocument();
      expect(
        screen.getByText(mockProductData.product_asin)
      ).toBeInTheDocument();
    });

    expect(global.fetch).toHaveBeenCalledWith(
      `${process.env.NEXT_PUBLIC_BACKEND_API}/product/123`
    );
  });

  it("displays reviews when product data is loaded", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockProductData,
    });

    render(<ProductOverview {...mockProps} />);

    await waitFor(() => {
      expect(screen.getByText("Customer Reviews")).toBeInTheDocument();
      expect(screen.getByText("Great product")).toBeInTheDocument();
      expect(screen.getByText("Good but could be better")).toBeInTheDocument();
    });
  });

  it("handles fetch error correctly", async () => {
    const error = new Error("Failed to fetch");
    (global.fetch as jest.Mock).mockRejectedValueOnce(error);

    render(<ProductOverview {...mockProps} />);

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith(
        `Error fetching product data: ${error}.`
      );
    });
  });

  it("handles API error response correctly", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
    });

    render(<ProductOverview {...mockProps} />);

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith(
        "Error fetching product data: Error: Failed to fetch product data."
      );
    });
  });
});
