"use client";

import { motion } from "framer-motion";
import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";

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

export function Features() {
  return (
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
  );
}
