import { FC } from "react";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";

interface BenefitProps {
  title: string;
  description: string;
}

const Benefit: FC<BenefitProps> = ({ title, description }) => (
  <Card className="p-6">
    <Text variant="h3" className="mb-2 text-lg font-semibold">
      {title}
    </Text>
    <Text className="text-gray-600">{description}</Text>
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
    <section className="w-full py-24 bg-gray-50">
      <div className="container mx-auto px-4">
        <Text variant="h2" className="text-center mb-12">
          Why Neuromosaic?
        </Text>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
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
