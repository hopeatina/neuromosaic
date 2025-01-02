"use client";

import Image from "next/image";
import { HTMLAttributes } from "react";
import { cn } from "@/library/utils";

interface LogoProps extends HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg" | "xl";
  variant?: "light" | "dark";
  height?: number;
}

const sizeClasses = {
  sm: "w-8 h-8",
  md: "w-12 h-12",
  lg: "w-16 h-16",
  xl: "w-64 h-64",
};

export function Logo({
  className,
  size = "md",
  variant = "dark",
  ...props
}: LogoProps) {
  return (
    <div className={cn("relative", sizeClasses[size], className)} {...props}>
      <Image
        src="/images/neuromosaic_logo.png"
        alt="Neuromosaic Logo"
        fill
        className="object-contain"
        priority
      />
    </div>
  );
}

export type { LogoProps };
