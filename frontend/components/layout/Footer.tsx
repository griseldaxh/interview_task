import Image from "next/image";
import Link from "next/link";

import FacebookLogo from "@/components/svg/FacebookLogo";
import LinkedinLogo from "@/components/svg/LinkedinLogo";
import TwitterLogo from "@/components/svg/TwitterLogo";
import { Button } from "@/components/ui/Button";

const NavLinks = [
  { href: "/products", label: "Products" },
  { href: "/", label: "Reviews" },
];

const SocialLinks = [
  { href: "https://facebook.com", label: "Facebook", Icon: FacebookLogo },
  { href: "https://linkedin.com", label: "LinkedIn", Icon: LinkedinLogo },
  { href: "https://twitter.com", label: "Twitter", Icon: TwitterLogo },
];

export default function Footer() {
  return (
    <footer className="bg-black py-8 text-white">
      <div className="mx-auto max-w-6xl px-8">
        <nav className="mb-8 flex justify-center space-x-6">
          {NavLinks.map((link) => (
            <Button variant="link" key={link.label}>
              <Link href={link.href}>{link.label}</Link>
            </Button>
          ))}
        </nav>
        <div className="border-t border-zinc-600 pt-8">
          <div className="flex flex-col items-center justify-between md:flex-row">
            <div className="mb-4 flex items-center md:mb-0">
              <Link href="/" className="flex items-center"></Link>
              <div className="flex items-center gap-2">
                <Image
                  src="data:image/png;base64,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"
                  alt="SellerX Logo"
                  className="h-8 w-auto"
                  width={32}
                  height={32}
                />
                <span className="font-medium text-[18px]">SellerX</span>
              </div>
            </div>

            <div className="mt-4 flex items-center space-x-4 md:mt-0">
              {SocialLinks.map(({ href, label, Icon }) => (
                <a
                  key={label}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="transition-colors hover:text-gray-300"
                  aria-label={label}
                >
                  <Icon />
                </a>
              ))}
            </div>
          </div>
          <p className="text-center text-sm text-zinc-400 mt-2">
            Copyright © {new Date().getFullYear()} SellerX.com
          </p>
        </div>
      </div>
    </footer>
  );
}
