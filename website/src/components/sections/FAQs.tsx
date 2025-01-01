"use client";

import { FC } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { useState } from "react";

interface FAQProps {
  question: string;
  answer: string | string[];
  index: number;
}

const FAQ: FC<FAQProps> = ({ question, answer, index }) => {
  const [isOpen, setIsOpen] = useState(false);

  const formattedAnswer = Array.isArray(answer) ? (
    <ul className="list-disc pl-6 space-y-2">
      {answer.map((item, index) => (
        <li key={index}>{item}</li>
      ))}
    </ul>
  ) : (
    answer
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      viewport={{ once: true }}
    >
      <Card
        className={`
          group p-6 transition-all duration-300 cursor-pointer 
          hover:shadow-md border border-gray-100
          ${isOpen ? "bg-gray-50/80" : "bg-white/80"}
          backdrop-blur-sm
        `}
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex justify-between items-start gap-4">
          <Text
            variant="h3"
            className="text-lg font-semibold text-gray-900 group-hover:text-primary transition-colors duration-300"
          >
            {question}
          </Text>
          <motion.button
            animate={{ rotate: isOpen ? 180 : 0 }}
            transition={{ duration: 0.3 }}
            className="flex-shrink-0 w-6 h-6 flex items-center justify-center text-gray-500 group-hover:text-primary transition-colors duration-300"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="w-4 h-4"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </motion.button>
        </div>
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <Text className="mt-4 text-gray-600">{formattedAnswer}</Text>
            </motion.div>
          )}
        </AnimatePresence>
      </Card>
    </motion.div>
  );
};

const faqs = [
  {
    question: "What is Neuromosaic?",
    answer:
      "Neuromosaic is a distributed platform for training and improving AI models through iterative refinement and community collaboration. Think of it as a global laboratory where anyone can contribute compute power, model ideas, or experiments to push machine learning research forward.",
  },
  {
    question: "How does Neuromosaic work in simple terms?",
    answer: [
      "Sign Up: Create an account and configure your local environment or cloud setup.",
      "Select or Create an Experiment: Choose from existing experiments or propose a new research idea.",
      "Contribute & Collaborate: Run experiments locally (or in the cloud) and sync your results.",
      "Refine & Iterate: Analyze aggregated results, get suggestions for next steps, and repeat.",
      "The platform automates much of the complexity, so you can focus on experimenting and innovating rather than heavy setup.",
    ],
  },
  {
    question: "Do I need a powerful computer or GPU to participate?",
    answer:
      "Not necessarily! Neuromosaic is designed to scale across different resource levels. If you have a GPU, that's great—you can train larger models or more intensive experiments. If you only have a CPU, you can still participate by running smaller jobs or by contributing to tasks that require less compute. Every bit of participation helps the community.",
  },
  {
    question: "Is Neuromosaic free to use?",
    answer:
      "Yes. The core platform is open-source and free to join, meaning that anyone can sign up, run experiments, and benefit from shared research. There may be optional premium or enterprise services in the future, but the base platform will remain accessible to all.",
  },
  {
    question:
      "How do I integrate Neuromosaic into my existing workflow or tools?",
    answer:
      "Neuromosaic provides a Command-Line Interface (CLI) and documentation for connecting to various ML frameworks (e.g., PyTorch or TensorFlow). You can clone our GitHub repository, follow the setup instructions, and plug Neuromosaic into your current training or data pipelines. We also offer an API layer for more advanced integration with custom tools or dashboards.",
  },
  {
    question: "Can I use my own datasets and custom algorithms?",
    answer:
      "Absolutely! Neuromosaic is designed for openness and extendibility. You can upload or connect your datasets, then run experiments with your own algorithms or modifications. The platform's architecture makes it easy to insert custom code, test it, and share the results in a structured way.",
  },
  {
    question: "How are results shared and stored?",
    answer:
      "All experiment results can be synced securely to a global results index. This central repository allows others to discover, reuse, and build upon your findings. However, you can also keep certain experiments private if you're working on sensitive or proprietary data.",
  },
  {
    question: "What about security and data privacy?",
    answer:
      "We take security very seriously. Neuromosaic uses secure authentication (via SSO or standard login) and encrypted channels for data transfers. You can also deploy Neuromosaic on your own infrastructure if you want total control over data privacy. See our Security Documentation for more details.",
  },
  {
    question: "How do I get support if I run into issues?",
    answer: [
      "Community Forum / Discord / Slack: Ask questions, report bugs, and get tips from other users and contributors.",
      "GitHub Issues: Open a ticket on our repo for technical support or feature requests.",
      "Email Support: For urgent matters or private queries, you can contact our core team via email.",
    ],
  },
  {
    question: "Who can I collaborate with on Neuromosaic?",
    answer:
      "Anyone! Our community includes students, independent researchers, professionals in industry, and hobbyists. Neuromosaic is designed to bring together people with diverse backgrounds to accelerate AI innovation. You can join team experiments, share your findings, or help others refine their models.",
  },
  {
    question: "How do I stay updated on new features or important changes?",
    answer:
      "We regularly post updates on our GitHub and Twitter. You can also subscribe to our newsletter or check out our 'Updates' page for roadmap highlights and upcoming features.",
  },
  {
    question: "Where can I find more detailed documentation?",
    answer:
      "Check out our Docs page for step-by-step setup guides, best practices for running experiments, tips for managing data, and more. We continuously add new tutorials and resources to help you get the most out of Neuromosaic.",
  },
];

export const FAQs: FC = () => {
  return (
    <section className="w-full py-16 md:py-24 bg-gradient-to-b from-gray-50 to-white">
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
              Common Questions About Neuromosaic
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="mt-4 max-w-2xl mx-auto text-center"
            >
              Find answers to frequently asked questions about our platform,
              from getting started to advanced usage. Our comprehensive guide
              helps you understand how Neuromosaic can enhance your AI
              development workflow.
            </Text>
          </motion.div>
        </div>

        <div className="max-w-3xl mx-auto space-y-4">
          {faqs.map((faq, index) => (
            <FAQ key={index} {...faq} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
};
