import { FC } from "react";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { motion } from "framer-motion";

interface BenefitProps {
  title: string;
  description: string;
}

const Benefit: FC<BenefitProps> = ({ title, description }) => (
  <Card className="group p-6 hover:shadow-lg transition-shadow duration-300 bg-white/80 backdrop-blur-sm">
    <Text variant="h3" className="mb-3 text-lg font-semibold text-primary">
      {title}
    </Text>
    <Text className="text-gray-600 group-hover:text-gray-800 transition-colors duration-300">
      {description}
    </Text>
  </Card>
);

const benefits = [
  {
    title: "Distributed Training",
    description:
      "Leverage collective computing power to handle large-scale experiments.",
  },
  {
    title: "Community-Driven Innovation",
    description:
      "Collaborate with peers worldwide to push ML frontiers faster.",
  },
  {
    title: "Iterative Refinement",
    description:
      "Systematic experimentation ensures continuous improvement of models.",
  },
  {
    title: "Lower Barriers to Entry",
    description:
      "Designed so that both beginners and veterans can contribute effectively.",
  },
  {
    title: "Sharable Results & Insights",
    description: "Publish your model improvements for others to build upon.",
  },
];

export const WhyNeuromosaic: FC = () => {
  return (
    <section className="relative w-full py-16 md:py-24 bg-gradient-to-b from-gray-50 to-white">
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
              Why Choose Neuromosaic
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="mt-4 max-w-2xl mx-auto text-center"
            >
              Experience the power of collaborative AI development through our
              distributed platform, where innovation meets community-driven
              progress to reshape the future of machine learning.
            </Text>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 max-w-7xl mx-auto">
          {benefits.map((benefit, index) => (
            <Benefit
              key={index}
              title={benefit.title}
              description={benefit.description}
            />
          ))}
        </div>
      </div>
    </section>
  );
};
