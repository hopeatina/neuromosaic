"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Text } from "@/components/ui/Text";
import { Logo } from "@/components/ui/Logo";
import { FloatingPetal } from "@/components/ui/FloatingPetal";

const features = [
  {
    name: "Iterative Refinement",
    description:
      "Continuously improve AI models through a systematic process of training, testing, and refinement.",
  },
  {
    name: "Distributed Computing",
    description:
      "Leverage the power of distributed computing to accelerate model training and experimentation.",
  },
  {
    name: "Community Driven",
    description:
      "Join a community of researchers and developers working together to advance AI capabilities.",
  },
  {
    name: "Open Source",
    description:
      "Built on open-source principles, enabling transparency and collaborative development.",
  },
];

export default function Home() {
  return (
    <main className="relative">
      {/* Hero section */}
      <section className="relative isolate overflow-hidden min-h-[calc(100vh-4rem)] flex items-center">
        {/* Background gradient */}
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(45rem_50rem_at_top,theme(colors.primary.DEFAULT),theme(colors.background.dark))]" />

        {/* Floating petals */}
        <div className="absolute inset-0 -z-5 overflow-hidden">
          {/* Large petal top left */}
          <FloatingPetal
            size="xl"
            className="absolute -top-40 -left-20"
            gradientId="petal-1"
          />

          {/* Medium petal top right */}
          <FloatingPetal
            size="lg"
            className="absolute -top-20 -right-20"
            gradientId="petal-2"
            delay={1}
          />

          {/* Small petal bottom left */}
          <FloatingPetal
            size="md"
            className="absolute bottom-40 left-20"
            gradientId="petal-3"
            delay={2}
          />

          {/* Extra small petal bottom right */}
          <FloatingPetal
            size="sm"
            className="absolute bottom-20 right-40"
            gradientId="petal-4"
            delay={3}
          />

          {/* Additional background petals */}
          <FloatingPetal
            size="sm"
            className="absolute top-1/3 left-1/4"
            gradientId="petal-5"
            delay={0.5}
          />
          <FloatingPetal
            size="md"
            className="absolute top-2/3 right-1/4"
            gradientId="petal-6"
            delay={1.5}
          />
        </div>

        {/* Hero content */}
        <Container className="relative flex items-center justify-center w-full py-24 sm:py-32">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mx-auto max-w-3xl text-center flex flex-col items-center"
          >
            {/* Logo with floating animation */}
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

            {/* Main headline */}
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

            {/* CTA buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="flex flex-wrap justify-center gap-4"
            >
              <Link href="/get-involved" className="inline-block">
                <Button size="lg">Join the Waitlist</Button>
              </Link>
              <Link href="/about" className="inline-block">
                <Button variant="secondary" size="lg">
                  Learn More
                </Button>
              </Link>
            </motion.div>
          </motion.div>
        </Container>

        {/* Wave divider */}
        <div className="absolute bottom-0 left-0 right-0 text-background">
          <svg
            className="w-full h-24 fill-current"
            viewBox="0 0 1440 74"
            preserveAspectRatio="none"
          >
            <path d="M0,0 C480,74 960,74 1440,0 L1440,74 L0,74 Z" />
          </svg>
        </div>
      </section>

      {/* Features section */}
      <section className="relative bg-background">
        <Container className="py-24 sm:py-32">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="mx-auto max-w-2xl text-center"
          >
            <Text as="h2" variant="h1" className="mb-4">
              Advancing AI Through Collaboration
            </Text>
            <Text variant="body-lg" textColor="muted" className="mb-16">
              Our platform combines distributed computing with community-driven
              development to create more capable AI models.
            </Text>
          </motion.div>

          {/* Feature grid */}
          <div className="mx-auto max-w-7xl">
            <motion.div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.name}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.15 }}
                  viewport={{ once: true }}
                  className="relative"
                >
                  <Text as="h3" variant="h3" className="mb-3">
                    {feature.name}
                  </Text>
                  <Text textColor="muted">{feature.description}</Text>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </Container>
      </section>
    </main>
  );
}
