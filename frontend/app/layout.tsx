import type { Metadata } from "next";
import { inter, raleway } from "@/config/fonts";
import { Toaster } from "@/components/ui/toaster";
import type { LayoutProps } from "@/types/layout";
import "./globals.css";

export const metadata: Metadata = {
  title: "SellerX",
  description:
    "We buy and build Amazon businesses, helping entrepreneurs realise the next stage of their businesses, and their lives.",
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/favicon.png", type: "image/png" },
    ],
  },
};

export default function RootLayout({ children }: LayoutProps) {
  return (
    <html lang="en" className={`${inter.variable} ${raleway.variable}`}>
      <body>
        <main className="flex w-full flex-col items-center justify-center h-screen">
          <div className="flex flex-col w-full h-full">{children}</div>
          <Toaster position="top-right" />
        </main>
      </body>
    </html>
  );
}
