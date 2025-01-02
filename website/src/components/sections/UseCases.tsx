"use client";

import { FC } from "react";
import { motion } from "framer-motion";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { GraduationCap, Rocket, Code2 } from "lucide-react";

interface UseCaseProps {
  title: string;
  description: string;
  index: number;
  icon: React.ReactNode;
}

const UseCase: FC<UseCaseProps> = ({ title, description, index, icon }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay: index * 0.1 }}
    viewport={{ once: true }}
  >
    <Card className="group h-full p-8 hover:shadow-lg transition-all duration-300 bg-white/80 backdrop-blur-sm border border-gray-100">
      <div className="flex items-start gap-4">
        <div className="p-2 rounded-lg bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors duration-300">
          {icon}
        </div>
        <div>
          <Text
            variant="h3"
            className="text-xl font-semibold mb-4 text-primary group-hover:text-primary/80 transition-colors duration-300"
          >
            {title}
          </Text>
          <Text className="text-gray-600 group-hover:text-gray-700 transition-colors duration-300">
            {description}
          </Text>
        </div>
      </div>
    </Card>
  </motion.div>
);

const useCases = [
  {
    title: "Academic Researchers",
    description:
      "Tap into a global ML community to run large-scale experiments you couldn't otherwise afford.",
    icon: <GraduationCap size={24} />,
  },
  {
    title: "Startups",
    description:
      "Accelerate innovation by accessing shared knowledge and compute without building everything from scratch.",
    icon: <Rocket size={24} />,
  },
  {
    title: "Independent ML Enthusiasts",
    description:
      "Experiment with cutting-edge models in a supportive environment—level up your skills while contributing real value.",
    icon: <Code2 size={24} />,
  },
];

export const UseCases: FC = () => {
  return (
    <section className="w-full py-16 md:py-24 bg-primary-faded">
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
              Success Stories & Applications
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="mt-4 max-w-2xl mx-auto text-center"
            >
              Discover how diverse teams across academia, industry, and the
              open-source community are leveraging Neuromosaic to push the
              boundaries of AI innovation and research.
            </Text>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 max-w-7xl mx-auto">
          {useCases.map((useCase, index) => (
            <UseCase
              key={index}
              index={index}
              title={useCase.title}
              description={useCase.description}
              icon={useCase.icon}
            />
          ))}
        </div>
      </div>
    </section>
  );
};
