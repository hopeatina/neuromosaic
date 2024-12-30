"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

// Petal color combos
const petalColors = [
  {
    start: "#2e2066", // Deep purple
    mid: "#bf3abb", // Vibrant pink
    end: "#0c0c1c", // Midnight blue
  },
  {
    start: "#3b82f6", // Blue
    mid: "#6366f1", // Indigo
    end: "#2e2066", // Deep purple
  },
  {
    start: "#ec4899", // Pink
    mid: "#d946ef", // Fuschia
    end: "#6366f1", // Indigo
  },
  {
    start: "#bf3abb", // Vibrant pink
    mid: "#9333ea", // Purple
    end: "#2e2066", // Deep purple
  },
];

// Define size classes for the container
const sizeClasses = {
  sm: "w-[200px] h-[200px]",
  md: "w-[300px] h-[300px]",
  lg: "w-[400px] h-[400px]",
  xl: "w-[500px] h-[500px]",
};

interface FloatingPetalProps {
  className?: string;
  size?: "sm" | "md" | "lg" | "xl";
  delay?: number;
  gradientId?: string;
  randomness?: boolean; // Optional: toggle random color/rotation
}

export function FloatingPetal({
  className,
  size = "md",
  delay = 0,
  gradientId = "petal",
  randomness = true,
}: FloatingPetalProps) {
  // If randomness is enabled, pick a random color combo
  const colors = randomness
    ? petalColors[Math.floor(Math.random() * petalColors.length)]
    : petalColors[0]; // fallback if not random

  // Subtle random rotation and scale (less extreme than before)
  const initialRotation = randomness ? Math.random() * 60 - 30 : 0; // -30 to +30 deg
  const scaleVariation = randomness ? 0.95 + Math.random() * 0.1 : 1; // 0.95 to 1.05
  const moveRange = randomness ? Math.random() * 30 - 15 : 0; // -15 to +15 px

  return (
    <motion.div
      initial={{
        y: 0,
        rotate: initialRotation,
        scale: 1,
      }}
      animate={{
        y: [0, moveRange, 0],
        rotate: [initialRotation, initialRotation + 10, initialRotation],
        scale: [1, scaleVariation, 1],
      }}
      transition={{
        duration: 10, // slightly slower
        repeat: Infinity,
        ease: "easeInOut",
        delay: delay,
      }}
      className={cn(sizeClasses[size], "relative", className)}
    >
      <svg
        viewBox="0 0 500 500"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full"
      >
        <defs>
          {/* 
            A radial gradient with multiple stops for smoother transitions 
            (e.g. 0%, 35%, 70%, 100%) 
          */}
          <radialGradient id={gradientId} cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor={colors.start} stopOpacity="0.85" />
            <stop offset="35%" stopColor={colors.mid} stopOpacity="0.4" />
            <stop offset="70%" stopColor={colors.mid} stopOpacity="0.25" />
            <stop offset="100%" stopColor={colors.end} stopOpacity="0.15" />
          </radialGradient>

          <filter
            id={`${gradientId}-blur`}
            x="-50%"
            y="-50%"
            width="200%"
            height="200%"
          >
            <feGaussianBlur in="SourceGraphic" stdDeviation="4" />
          </filter>
        </defs>

        {/* Outer swirl shape: a layered, overlapping path reminiscent of petals */}
        <g filter={`url(#${gradientId}-blur)`}>
          <path
            d="
              M250,60
              C320,50 380,80 410,150
              C440,210 420,280 380,320
              C330,370 270,390 210,370
              C160,350 130,310 90,260
              C60,220 50,170 70,130
              C100,70 160,50 250,60
              Z
            "
            fill={`url(#${gradientId})`}
          />

          {/* A second, smaller "inner swirl" shape to add depth */}
          <path
            d="
              M250,140
              C290,130 330,160 350,200
              C370,240 360,290 320,320
              C280,350 220,350 180,320
              C150,290 130,240 140,200
              C150,160 210,130 250,140
              Z
            "
            fill={`url(#${gradientId})`}
            fillOpacity="0.6"
          />
        </g>
      </svg>
    </motion.div>
  );
}
