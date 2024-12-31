import { FC } from "react";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";

interface UseCaseProps {
  title: string;
  description: string;
}

const UseCase: FC<UseCaseProps> = ({ title, description }) => (
  <Card className="p-8">
    <Text variant="h3" className="text-xl font-semibold mb-4">
      {title}
    </Text>
    <Text className="text-gray-600">{description}</Text>
  </Card>
);

const useCases = [
  {
    title: "Academic Researchers",
    description:
      "Tap into a global ML community to run large-scale experiments you couldn't otherwise afford.",
  },
  {
    title: "Startups",
    description:
      "Accelerate innovation by accessing shared knowledge and compute without building everything from scratch.",
  },
  {
    title: "Independent ML Enthusiasts",
    description:
      "Experiment with cutting-edge models in a supportive environment—level up your skills while contributing real value.",
  },
];

export const UseCases: FC = () => {
  return (
    <section className="w-full py-24 bg-gray-50">
      <div className="container mx-auto px-4">
        <Text variant="h2" className="text-center mb-12">
          Use Cases & Success Stories
        </Text>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {useCases.map((useCase, index) => (
            <UseCase
              key={index}
              title={useCase.title}
              description={useCase.description}
            />
          ))}
        </div>
      </div>
    </section>
  );
};
