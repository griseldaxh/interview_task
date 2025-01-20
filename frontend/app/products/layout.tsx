import RoundedHeader from '@/components/layout/RoundedHeader';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen lg:bg-primary-light">
      <RoundedHeader />
      <main className="w-full flex flex-col items-center justify-center bg-white lg:bg-primary-light md:px-20">
        {children}
      </main>
    </div>
  );
}
