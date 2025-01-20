export const NavLinks: { href: string; label: string }[] = [
  { href: "/products", label: "Products" },
  { href: "/", label: "Reviews" },
];

// Animation constants
export const ANIMATION_CONFIG = {
  container: {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.5,
      },
    },
  },
  item: {
    hidden: { opacity: 0, y: 20 },
    show: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 1,
      },
    },
  },
} as const;
