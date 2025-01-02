"use client";

import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { motion } from "framer-motion";
import { Sparkles, Users, Cpu, BarChart3, GitMerge, Zap } from "lucide-react";
import Link from "next/link";
import type { FC } from "react";

interface UpdateCardProps {
  date: string;
  title: string;
  description: string;
  type: string;
  link: string;
  icon: React.ReactNode;
}

const UpdateCard: FC<UpdateCardProps> = ({
  date,
  title,
  description,
  type,
  link,
  icon,
}) => (
  <Link href={link}>
    <Card className="group h-full p-6 hover:shadow-lg transition-all duration-300 bg-white/80 backdrop-blur-sm border border-gray-100">
      <div className="flex justify-between items-start mb-4">
        <span className="inline-flex items-center gap-2 rounded-md bg-primary/10 px-2 py-1 text-sm font-medium text-primary">
          {icon}
          {type}
        </span>
        <Text variant="small" textColor="muted">
          {date}
        </Text>
      </div>
      <Text
        as="h3"
        variant="h3"
        className="mb-3 text-primary group-hover:text-primary/80 transition-colors duration-300"
      >
        {title}
      </Text>
      <Text
        textColor="muted"
        className="group-hover:text-gray-700 transition-colors duration-300"
      >
        {description}
      </Text>
    </Card>
  </Link>
);

const updates = [
  {
    date: "2024 Q1",
    title: "Distributed Training Beta",
    description:
      "Launch of our distributed training infrastructure beta program, enabling parallel model training across multiple nodes.",
    type: "feature",
    link: "/distributed",
    icon: <Sparkles size={16} />,
  },
  {
    date: "2024 Q1",
    title: "Community Contributions",
    description:
      "New contribution guidelines and documentation for community members looking to participate in development.",
    type: "community",
    link: "/docs/contributing",
    icon: <Users size={16} />,
  },
  {
    date: "2024 Q1",
    title: "Platform Architecture",
    description:
      "Major updates to our core platform architecture, improving scalability and resource utilization.",
    type: "technical",
    link: "/docs/architecture",
    icon: <Cpu size={16} />,
  },
];

interface RoadmapCardProps {
  quarter: string;
  items: string[];
  icon: React.ReactNode;
}

const RoadmapCard: FC<RoadmapCardProps> = ({ quarter, items, icon }) => (
  <Card className="group p-6 hover:shadow-lg transition-all duration-300 bg-white/80 backdrop-blur-sm border border-gray-100">
    <div className="flex items-start gap-4 mb-6">
      <div className="p-2 rounded-lg bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors duration-300">
        {icon}
      </div>
      <Text as="h3" variant="h3" className="text-primary">
        {quarter}
      </Text>
    </div>
    <ul className="space-y-4">
      {items.map((item) => (
        <li key={item} className="flex items-start gap-3">
          <span className="block w-2 h-2 mt-2 rounded-full bg-primary shrink-0" />
          <Text
            textColor="muted"
            className="group-hover:text-gray-700 transition-colors duration-300"
          >
            {item}
          </Text>
        </li>
      ))}
    </ul>
  </Card>
);

const roadmap = [
  {
    quarter: "Q2 2024",
    items: [
      "Enhanced monitoring and analytics dashboard",
      "Improved resource allocation algorithms",
      "Extended API documentation",
    ],
    icon: <BarChart3 size={24} />,
  },
  {
    quarter: "Q3 2024",
    items: [
      "Advanced model versioning system",
      "Automated performance optimization",
      "Community contribution rewards",
    ],
    icon: <GitMerge size={24} />,
  },
];

export default function UpdatesPage() {
  return (
    <div className="relative">
      {/* Hero section with gradient background */}
      <div className="relative min-h-[50vh] bg-gradient-to-b from-black via-background-dark to-primary-ultralight flex items-center">
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
              Platform Updates
            </Text>
            <Text
              variant="body-lg"
              textColor="white"
              className="mb-8 opacity-90 text-center"
            >
              Stay informed about the latest developments, features, and
              improvements to the Neuromosaic platform.
            </Text>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                href="https://neuromosaic.mintlify.app/"
                className="inline-block"
              >
                <Button
                  size="lg"
                  className="bg-white text-primary hover:bg-white/90"
                >
                  View Documentation
                </Button>
              </Link>
              <Link
                href="https://github.com/hopeatina/neuromosaic"
                className="inline-block"
              >
                <Button
                  variant="secondary"
                  size="lg"
                  className="bg-background-glass text-white border-2 border-white/20 hover:bg-background-glass-light hover:border-white/40"
                >
                  GitHub Releases
                </Button>
              </Link>
            </div>
          </motion.div>
        </Container>
      </div>

      {/* Recent Updates section */}
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
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="mb-12 text-center"
          >
            <Text
              as="h2"
              variant="h1"
              className="text-gradient mb-6 mx-auto text-center"
            >
              Recent Updates
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="max-w-2xl mx-auto text-center"
            >
              Stay up to date with our latest features, improvements, and
              community initiatives.
            </Text>
          </motion.div>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
            {updates.map((update, index) => (
              <motion.div
                key={update.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <UpdateCard {...update} />
              </motion.div>
            ))}
          </div>
        </Container>
      </div>

      {/* Roadmap section with gradient background */}
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
              Development Roadmap
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="max-w-2xl mx-auto text-center"
            >
              Our vision for the future of Neuromosaic, with planned features
              and improvements to enhance your collaborative AI development
              experience.
            </Text>
          </motion.div>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
            {roadmap.map((quarter, index) => (
              <motion.div
                key={quarter.quarter}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <RoadmapCard {...quarter} />
              </motion.div>
            ))}
          </div>
        </Container>
      </div>
    </div>
  );
}
