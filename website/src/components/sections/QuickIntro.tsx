"use client";

import { motion } from "framer-motion";
import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";

const highlights = [
  {
    title: "Distributed Training",
    description:
      "Leverage collective computing power to train and improve AI models at scale",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        className="w-6 h-6"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5"
        />
      </svg>
    ),
  },
  {
    title: "Community-Driven",
    description:
      "Join a network of researchers and developers collaborating on model improvements",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        className="w-6 h-6"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z"
        />
      </svg>
    ),
  },
  {
    title: "Iterative Refinement",
    description:
      "Continuously improve models through systematic experimentation and validation",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        className="w-6 h-6"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 00-3.7-3.7 48.678 48.678 0 00-7.324 0 4.006 4.006 0 00-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3l-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 003.7 3.7 48.656 48.656 0 007.324 0 4.006 4.006 0 003.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3l-3 3"
        />
      </svg>
    ),
  },
];

export function QuickIntro() {
  return (
    <section className="relative overflow-hidden bg-background-glass">
      {/* Decorative swirl */}
      <div className="absolute right-0 top-0 -z-10 w-[600px] h-[600px] opacity-10">
        <svg
          viewBox="0 0 600 600"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M300 550C439.787 550 550 439.787 550 300C550 160.213 439.787 50 300 50C160.213 50 50 160.213 50 300C50 439.787 160.213 550 300 550Z"
            stroke="url(#paint0_linear)"
            strokeWidth="20"
            strokeLinecap="round"
            strokeDasharray="1 50"
          />
          <defs>
            <linearGradient
              id="paint0_linear"
              x1="50"
              y1="300"
              x2="550"
              y2="300"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#2e2066" />
              <stop offset="1" stopColor="#bf3abb" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <Container className="py-24">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-2">
          {/* Left column */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <Text as="h2" variant="h2" className="mb-6">
              What is Neuromosaic?
            </Text>
            <Text variant="body-lg" textColor="muted" className="max-w-xl">
              Neuromosaic is a distributed platform that brings together
              researchers, developers, and AI enthusiasts to collaboratively
              train and improve machine learning models. By harnessing
              collective computing power and expertise, we&apos;re accelerating
              the development of more capable and reliable AI systems.
            </Text>
          </motion.div>

          {/* Right column */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            {highlights.map((highlight, index) => (
              <motion.div
                key={highlight.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="flex gap-4"
              >
                <div className="flex-shrink-0 w-12 h-12 flex items-center justify-center rounded-xl bg-primary/10 text-primary">
                  {highlight.icon}
                </div>
                <div>
                  <Text as="h3" variant="h4" className="mb-2">
                    {highlight.title}
                  </Text>
                  <Text textColor="muted">{highlight.description}</Text>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </Container>
    </section>
  );
}
