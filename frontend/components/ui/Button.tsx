import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-3xl text-md font-base transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-5 [&_svg]:shrink-0 dark:focus-visible:ring-neutral-white",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-neutral-white shadow hover:bg-primary/90 dark:bg-neutral-white dark:text-primary dark:hover:bg-neutral-white/90",
        destructive:
          "bg-red-500 text-neutral-white shadow-sm hover:bg-red-500/90 dark:bg-red-900 dark:text-neutral-white dark:hover:bg-red-900/90",
        outline:
          "border border-primary bg-transparent text-primary shadow-sm hover:bg-primary hover:text-neutral-white dark:border-neutral-white dark:bg-transparent dark:hover:bg-neutral-white dark:hover:text-primary",
        secondary:
          "bg-secondary text-neutral-white shadow-sm hover:bg-secondary/90 dark:bg-secondary/80 dark:text-neutral-white dark:hover:bg-secondary",
        ghost:
          "text-primary hover:bg-accent hover:text-primary dark:text-neutral-white dark:hover:bg-accent dark:hover:text-primary",
        link: "text-gray-200 hover:text-gray-400",
      },
      size: {
        default: "h-9 px-5 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";

export { Button, buttonVariants };
