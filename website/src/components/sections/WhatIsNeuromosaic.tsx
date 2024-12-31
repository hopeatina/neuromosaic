import { Text } from "@/components/ui/Text";
import { FC } from "react";

export const WhatIsNeuromosaic: FC = () => {
  return (
    <section className="w-full py-24 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <Text variant="h2" className="text-center mb-6">
            What Is Neuromosaic?
          </Text>

          <Text className="text-center text-gray-600 mb-12">
            Neuromosaic is a community-driven platform where researchers,
            developers, and enthusiasts come together to train and improve AI
            models in a distributed manner. By pooling computational resources
            and sharing knowledge, we iterate on ML models faster and make
            real-world impact accessible to everyone.
          </Text>

          {/* Video placeholder - replace with actual video component */}
          <div className="aspect-video bg-gray-100 rounded-lg shadow-md flex items-center justify-center">
            <Text className="text-gray-500">Explainer Video Coming Soon</Text>
          </div>
        </div>
      </div>
    </section>
  );
};
