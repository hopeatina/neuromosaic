"use client";

import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { Network, Database, GitBranch, LineChart } from "lucide-react";
import { motion } from "framer-motion";
import type { FC } from "react";

interface ArchitecturePointProps {
  title: string;
  description: string;
  icon: React.ReactNode;
}

const ArchitecturePoint: FC<ArchitecturePointProps> = ({
  title,
  description,
  icon,
}) => (
  <Card className="group p-6 hover:shadow-lg transition-all duration-300 bg-white/80 backdrop-blur-sm border border-gray-100">
    <div className="flex items-start gap-4">
      <div className="p-2 rounded-lg bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors duration-300">
        {icon}
      </div>
      <div>
        <Text as="h3" variant="h3" className="mb-3 text-primary">
          {title}
        </Text>
        <Text textColor="muted">{description}</Text>
      </div>
    </div>
  </Card>
);

const architecturePoints = [
  {
    title: "Distributed Training",
    description:
      "Our platform distributes model training across multiple nodes, enabling faster iteration and more comprehensive testing.",
    icon: <Network size={24} />,
  },
  {
    title: "Data Pipeline",
    description:
      "Efficient data processing and augmentation pipelines ensure high-quality training data for model improvement.",
    icon: <Database size={24} />,
  },
  {
    title: "Model Versioning",
    description:
      "Sophisticated version control for models, allowing easy tracking of improvements and rollbacks when needed.",
    icon: <GitBranch size={24} />,
  },
  {
    title: "Result Analysis",
    description:
      "Comprehensive analytics and visualization tools to understand model performance and identify areas for improvement.",
    icon: <LineChart size={24} />,
  },
];

export default function AboutPage() {
  return (
    <div className="relative">
      {/* Hero section with gradient background */}
      <div className="relative min-h-[60vh] bg-gradient-to-b from-black via-background-dark to-primary-ultralight flex items-center">
        <div className="absolute inset-0 bg-[radial-gradient(45rem_50rem_at_top,theme(colors.primary.DEFAULT),transparent)] opacity-30" />
        <Container className="relative z-10 py-16 sm:py-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mx-auto max-w-2xl text-center"
          >
            <Text
              as="h1"
              variant="display"
              textColor="white"
              className="mb-6 text-center"
            >
              About Neuromosaic
            </Text>
            <Text
              variant="body-lg"
              textColor="white"
              className="mb-8 opacity-90 text-center"
            >
              Neuromosaic is an open-source platform that enables distributed AI
              model training and refinement through community collaboration. Our
              goal is to accelerate AI development by combining distributed
              computing with collective expertise.
            </Text>
          </motion.div>
        </Container>
      </div>

      {/* Mission section with wave divider */}
      <div className="relative bg-secondary-ultralight">
        <div className="absolute top-0 left-0 right-0 transform -translate-y-full text-secondary-ultralight">
          <svg
            className="w-full h-24 fill-current"
            viewBox="0 0 1440 74"
            preserveAspectRatio="none"
          >
            <path d="M0,0 C480,74 960,74 1440,0 L1440,74 L0,74 Z" />
          </svg>
        </div>
        <Container className="py-24">
          <div className="grid grid-cols-1 gap-16 lg:grid-cols-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="text-center lg:text-left"
            >
              <Text
                as="h2"
                variant="h1"
                className="text-gradient mb-6 max-w-xl mx-auto lg:mx-0 text-center lg:text-left"
              >
                Our Mission
              </Text>
              <Text
                variant="body-lg"
                textColor="muted"
                className="mb-8 max-w-xl mx-auto lg:mx-0 text-center lg:text-left"
              >
                We believe that the future of AI development lies in
                collaborative efforts and distributed computing. By providing
                tools and infrastructure for the community to work together, we
                can accelerate the pace of innovation while ensuring
                transparency and ethical development.
              </Text>
              <div className="space-y-4 max-w-xl mx-auto lg:mx-0">
                <Text
                  variant="body"
                  textColor="muted"
                  className="text-center lg:text-left"
                >
                  Key objectives:
                </Text>
                <ul className="space-y-3 text-left">
                  {[
                    "Enable distributed model training and experimentation",
                    "Foster collaboration among researchers and developers",
                    "Maintain transparency in AI development",
                    "Accelerate the pace of AI innovation",
                  ].map((item, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <span className="block w-2 h-2 mt-2 rounded-full bg-primary shrink-0" />
                      <Text textColor="muted" className="text-left">
                        {item}
                      </Text>
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="text-center lg:text-left"
            >
              <Text
                as="h2"
                variant="h1"
                className="text-gradient mb-6 max-w-xl mx-auto lg:mx-0 text-center lg:text-left"
              >
                Why Distributed?
              </Text>
              <Text
                variant="body-lg"
                textColor="muted"
                className="mb-8 max-w-xl mx-auto lg:mx-0 text-center lg:text-left"
              >
                Distributed computing allows us to harness the collective power
                of many systems, leading to faster training times and more
                comprehensive testing. This approach also enables:
              </Text>
              <ul className="space-y-3 text-left max-w-xl mx-auto lg:mx-0">
                {[
                  "Parallel experimentation across multiple nodes",
                  "Efficient resource utilization",
                  "Scalable infrastructure for growing demands",
                  "Resilient and fault-tolerant operations",
                ].map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="block w-2 h-2 mt-2 rounded-full bg-primary shrink-0" />
                    <Text textColor="muted" className="text-left">
                      {item}
                    </Text>
                  </li>
                ))}
              </ul>
            </motion.div>
          </div>
        </Container>
      </div>

      {/* Architecture section with gradient background */}
      <div className="relative bg-accent-ultralight">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,theme(colors.accent.DEFAULT),transparent)] opacity-5" />
        <Container className="relative z-10 py-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <Text
              as="h2"
              variant="h1"
              className="text-gradient mb-6 mx-auto text-center"
            >
              Platform Architecture
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="max-w-2xl mx-auto text-center"
            >
              Our robust architecture is designed for scalability, reliability,
              and ease of use, enabling seamless collaboration across the
              community.
            </Text>
          </motion.div>
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {architecturePoints.map((point, index) => (
              <motion.div
                key={point.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <ArchitecturePoint {...point} />
              </motion.div>
            ))}
          </div>
        </Container>
      </div>
    </div>
  );
}
