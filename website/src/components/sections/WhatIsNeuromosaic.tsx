"use client";

import { Text } from "@/components/ui/Text";
import { motion } from "framer-motion";
import { FC } from "react";

export const WhatIsNeuromosaic: FC = () => {
  return (
    <section className="w-full py-16 md:py-24 bg-primary-ultralight">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="flex flex-col items-center mb-12 md:mb-16"
          >
            <Text as="h2" variant="h1" className="text-gradient text-center">
              What Is Neuromosaic?
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="mt-4 max-w-2xl mx-auto text-center"
            >
              Neuromosaic is a community-driven platform where researchers,
              developers, and enthusiasts come together to train and improve AI
              models in a distributed manner. By pooling computational resources
              and sharing knowledge, we iterate on ML models faster and make
              real-world impact accessible to everyone.
            </Text>
          </motion.div>

          {/* Video placeholder with animation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
            className="aspect-video bg-white/80 backdrop-blur-sm rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-300 flex items-center justify-center border border-gray-100"
          >
            <Text textColor="muted">Explainer Video Coming Soon</Text>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
