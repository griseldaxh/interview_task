import Footer from "@/components/layout/Footer";
import Header from "@/components/layout/Header";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <Header />
      <main className="bg-black flex flex-col flex-1 items-center justify-center px-6 pt-10 sm:px-10">
        {children}
      </main>
      <Footer />
    </>
  );
}
