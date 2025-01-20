"use client";

import { Menu, X } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { usePathname } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { NavLinks } from "@/lib/constants";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  const renderDesktopMenu = () => (
    <>
      <div className="hidden md:flex">
        {NavLinks.map((link) => (
          <Button
            variant="link"
            className={` ${pathname === link.href ? "font-semibold" : ""}`}
            key={link.label}
          >
            <Link href={link.href}>{link.label}</Link>
          </Button>
        ))}
      </div>
      <div className="hidden items-center gap-1 md:flex">
        <Button
          variant="link"
          className={`${pathname === "/" ? "font-semibold" : ""}`}
        >
          <Link href="/">Sign In</Link>
        </Button>
      </div>
    </>
  );

  const renderMobileMenu = () => (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center space-y-8 bg-black md:hidden">
      <button className="absolute right-5 top-6" onClick={toggleMenu}>
        <X size={24} />
      </button>
      {NavLinks.map((link) => (
        <Button
          variant="link"
          className={` ${pathname === link.href ? "font-semibold" : ""}`}
          key={link.label}
        >
          <Link href={link.href}>{link.label}</Link>
        </Button>
      ))}
    </div>
  );

  return (
    <nav className="sticky left-0 right-0 top-0 z-10 mx-auto w-full bg-primary px-6 py-6 text-white md:px-20">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <Link href="/" className="flex items-center">
          <div className="flex items-center gap-4">
            <Image
              src="data:image/png;base64,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"
              alt="SellerX Logo"
              className="h-10 w-auto"
              width={0}
              height={0}
            />
            <span className="text-2xl font-bold">SellerX</span>
          </div>
        </Link>
        {renderDesktopMenu()}
        <button className="md:hidden" onClick={toggleMenu}>
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>
      {isMenuOpen && renderMobileMenu()}
    </nav>
  );
};

export default Header;
