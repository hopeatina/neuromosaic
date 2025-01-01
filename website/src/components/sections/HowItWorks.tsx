"use client";

import { FC } from "react";
import { motion } from "framer-motion";
import { Text } from "@/components/ui/Text";

interface StepProps {
  number: number;
  title: string;
  description: string;
}

const Step: FC<StepProps> = ({ number, title, description }) => (
  <div className="group flex gap-6 items-start p-4 rounded-2xl hover:bg-gray-50 transition-colors duration-300">
    <div className="flex-shrink-0 w-12 h-12 bg-primary/90 group-hover:bg-primary shadow-md group-hover:shadow-lg rounded-xl flex items-center justify-center transition-all duration-300">
      <Text className="text-white font-bold">{number}</Text>
    </div>
    <div className="flex-1">
      <Text
        variant="h3"
        className="text-lg font-semibold mb-2 text-gray-900 group-hover:text-primary transition-colors duration-300"
      >
        {title}
      </Text>
      <Text className="text-gray-600 group-hover:text-gray-700 transition-colors duration-300">
        {description}
      </Text>
    </div>
  </div>
);

const steps = [
  {
    title: "Sign Up & Configure",
    description:
      "Create an account, set up your local environment or use your favorite cloud service.",
  },
  {
    title: "Select or Create an Experiment",
    description:
      "Browse existing experiments or propose a new idea to explore.",
  },
  {
    title: "Contribute Compute & Expertise",
    description:
      "Run training locally or on your organization's servers, then sync results.",
  },
  {
    title: "Analyze & Iterate",
    description:
      "NeuroMosaic aggregates experiment outputs, surfaces insights, and suggests next steps.",
  },
  {
    title: "Publish & Collaborate",
    description:
      "Share your improved model, get feedback from peers, and contribute to someone else's experiment.",
  },
];

export const HowItWorks: FC = () => {
  return (
    <section className="w-full py-16 md:py-24 bg-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="flex flex-col items-center mb-12 md:mb-16"
          >
            <Text as="h2" variant="h1" className="text-gradient text-center">
              Getting Started with Neuromosaic
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="mt-4 max-w-2xl mx-auto text-center"
            >
              Begin your journey in collaborative AI development with our
              streamlined process, designed to make advanced machine learning
              accessible to everyone, from beginners to experts.
            </Text>
          </motion.div>
        </div>

        <div className="max-w-3xl mx-auto space-y-6 md:space-y-8">
          {steps.map((step, index) => (
            <Step
              key={index}
              number={index + 1}
              title={step.title}
              description={step.description}
            />
          ))}
        </div>
      </div>
    </section>
  );
};
