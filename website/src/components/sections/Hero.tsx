"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Text } from "@/components/ui/Text";
import { Logo } from "@/components/ui/Logo";
import { NeuromosaicBlobs } from "@/components/gl/NeuromosaicBlobs";
import type { FC, HTMLProps } from "react";

interface HeroProps {
  onWaitlistClick: () => void;
}

export const Hero: FC<HeroProps> = ({ onWaitlistClick }) => {
  return (
    <div
      className="
        relative 
        isolate 
        min-h-[calc(100vh-4rem)] 
        overflow-hidden 
        /* No flex here at the top level to avoid pushing the canvas */
      "
    >
      {/* 
        1) The advanced WebGL background
        absolute + full coverage 
      */}
      <div className="absolute inset-0 -z-10">
        <NeuromosaicBlobs />
      </div>

      {/* 
        2) Optional fallback radial gradient 
        behind the canvas or as a partial overlay 
      */}
      <div
        className="
          absolute 
          inset-0 
          pointer-events-none 
          -z-10 
          bg-[radial-gradient(45rem_50rem_at_top,theme(colors.primary.DEFAULT),theme(colors.background.dark))]
          opacity-50
        "
      />

      {/* 
        3) Hero content container 
        relative + z-10 so it sits above the background 
      */}
      <div
        className="
          relative 
          z-10 
          flex 
          items-center 
          justify-center 
          min-h-[calc(100vh-4rem)]
          w-full
        "
      >
        <Container className="py-24 sm:py-32 align-center items-center">
          <div className="mx-auto max-w-3xl text-center flex flex-col items-center">
            {/* Floating Logo */}
            <motion.div
              initial={{ y: 0 }}
              animate={{ y: [-10, 10, -10] }}
              transition={{
                duration: 6,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="flex justify-center mb-8"
            >
              <Logo size="lg" />
            </motion.div>

            {/* Headline */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="w-full"
            >
              <Text
                as="h1"
                variant="display"
                textColor="white"
                className="mx-auto mb-6 text-center"
              >
                Train and Improve AI Models Through Community Collaboration
              </Text>
            </motion.div>

            {/* Subtext */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="w-full"
            >
              <Text
                variant="body-lg"
                textColor="white"
                className="max-w-2xl mx-auto mb-8 opacity-80"
              >
                Join our distributed platform for iterative AI model refinement.
                Contribute to the future of machine learning through
                collaborative experimentation.
              </Text>
            </motion.div>

            {/* CTAs */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="flex flex-wrap justify-center gap-4"
            >
              <Button size="lg" onClick={onWaitlistClick}>
                Join the Waitlist
              </Button>
              <Link href="/about" className="inline-block">
                <Button
                  variant="ghost"
                  size="lg"
                  className="
                    bg-background-glass 
                    hover:bg-background-glass-light 
                    text-white 
                    border-2 
                    border-secondary/20 
                    hover:border-secondary/40
                  "
                >
                  Learn More
                </Button>
              </Link>
            </motion.div>
          </div>
        </Container>
      </div>

      {/* Wave divider (optional) */}
      <div className="absolute bottom-0 left-0 right-0 text-background">
        <svg
          className="w-full h-24 fill-current"
          viewBox="0 0 1440 74"
          preserveAspectRatio="none"
        >
          <path d="M0,0 C480,74 960,74 1440,0 L1440,74 L0,74 Z" />
        </svg>
      </div>
    </div>
  );
};
