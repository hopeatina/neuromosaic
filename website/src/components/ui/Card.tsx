"use client";

import { HTMLAttributes, forwardRef } from "react";
import { VariantProps, cva } from "class-variance-authority";
import { cn } from "@/library/utils";

/**
 * We'll add a new "flywheel" variant that includes:
 * - A translucent background
 * - A fixed width/height
 * - Overflow auto (so longer text can scroll internally)
 */
const cardVariants = cva("rounded transition-shadow duration-200", {
  variants: {
    variant: {
      default: "bg-white shadow-card hover:shadow-card-hover",
      outline: "border border-neutral-200 hover:border-primary",
      ghost: "hover:bg-neutral-100",
      flywheel:
        "bg-white/80 backdrop-blur-md shadow-md hover:shadow-lg w-[230px] h-[220px] overflow-auto",
    },
    padding: {
      none: "",
      sm: "p-4",
      md: "p-6",
      lg: "p-8",
    },
  },
  defaultVariants: {
    variant: "default",
    padding: "md",
  },
});

export interface CardProps
  extends HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant, padding, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(cardVariants({ variant, padding, className }))}
        {...props}
      />
    );
  }
);

Card.displayName = "Card";
