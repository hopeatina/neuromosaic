"use client";

import { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface LogoProps extends HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg";
  variant?: "light" | "dark";
}

const sizeClasses = {
  sm: "w-8 h-8",
  md: "w-12 h-12",
  lg: "w-16 h-16",
};

export function Logo({
  className,
  size = "md",
  variant = "dark",
  ...props
}: LogoProps) {
  const isLight = variant === "light";

  return (
    <div className={cn("relative", sizeClasses[size], className)} {...props}>
      {/* Base circle with gradient */}
      <div
        className={cn(
          "absolute inset-0 rounded-full transition-opacity duration-200",
          isLight ? "opacity-90" : "opacity-100",
          "bg-gradient-primary"
        )}
      />

      {/* Overlapping petals */}
      <div className="absolute inset-0">
        {[0, 60, 120, 180, 240, 300].map((rotation, index) => (
          <div
            key={rotation}
            className={cn(
              "absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2",
              "w-[70%] h-[70%] rounded-full",
              "transform origin-center transition-all duration-300",
              "bg-gradient-to-br",
              index % 2 === 0
                ? "from-primary to-accent/80"
                : "from-accent to-primary/80",
              "hover:scale-110",
              isLight ? "opacity-90" : "opacity-80"
            )}
            style={{
              transform: `translate(-50%, -50%) rotate(${rotation}deg)`,
            }}
          />
        ))}
      </div>

      {/* Center circle with text */}
      <div
        className={cn(
          "absolute inset-0 flex items-center justify-center rounded-full",
          "transform scale-[0.4] transition-colors duration-200",
          isLight
            ? "bg-white text-background-dark"
            : "bg-background-dark text-white"
        )}
      >
        <span className="text-[0.5em] font-bold whitespace-nowrap">
          Neuromosaic
        </span>
      </div>

      {/* Glow effect */}
      <div
        className={cn(
          "absolute inset-0 rounded-full blur-lg transition-opacity duration-200",
          isLight ? "opacity-40" : "opacity-20",
          "bg-gradient-glow from-accent-light to-transparent"
        )}
      />
    </div>
  );
}

export type { LogoProps };
