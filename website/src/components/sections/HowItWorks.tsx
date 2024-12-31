import { FC } from "react";
import { Text } from "@/components/ui/Text";

interface StepProps {
  number: number;
  title: string;
  description: string;
}

const Step: FC<StepProps> = ({ number, title, description }) => (
  <div className="flex gap-6 items-start">
    <div className="flex-shrink-0 w-12 h-12 bg-primary rounded-full flex items-center justify-center">
      <Text className="text-white font-bold">{number}</Text>
    </div>
    <div>
      <Text variant="h3" className="text-lg font-semibold mb-2">
        {title}
      </Text>
      <Text className="text-gray-600">{description}</Text>
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
    <section className="w-full py-24 bg-white">
      <div className="container mx-auto px-4">
        <Text variant="h2" className="text-center mb-12">
          How It Works
        </Text>

        <div className="max-w-3xl mx-auto space-y-12">
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
