import Link from "next/link";
import { useState } from "react";
import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { WaitlistForm } from "@/components/forms/WaitlistForm";

const contributionAreas = [
  {
    title: "Model Development",
    description:
      "Contribute to core model architecture, training optimizations, and capability enhancements. Help shape the future of distributed AI training.",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        className="w-6 h-6"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
        />
      </svg>
    ),
    benefits: [
      "Access to cutting-edge AI research",
      "Collaboration with expert researchers",
      "Recognition for contributions",
      "Early access to new features",
    ],
  },
  {
    title: "Infrastructure",
    description:
      "Help build and optimize our distributed computing infrastructure. Work on scalability, reliability, and performance improvements.",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        className="w-6 h-6"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M5.25 14.25h13.5m-13.5 0a3 3 0 01-3-3m3 3a3 3 0 100 6h13.5a3 3 0 100-6m-16.5-3a3 3 0 013-3h13.5a3 3 0 013 3m-19.5 0a4.5 4.5 0 01.9-2.7L5.737 5.1a3.375 3.375 0 012.7-1.35h7.126c1.062 0 2.062.5 2.7 1.35l2.587 3.45a4.5 4.5 0 01.9 2.7m0 0a3 3 0 01-3 3m0 3h.008v.008h-.008v-.008zm0-6h.008v.008h-.008v-.008zm-3 6h.008v.008h-.008v-.008zm0-6h.008v.008h-.008v-.008z"
        />
      </svg>
    ),
    benefits: [
      "Work with modern cloud technologies",
      "Solve complex scaling challenges",
      "Impact platform performance",
      "Technical mentorship",
    ],
  },
  {
    title: "Documentation",
    description:
      "Create and improve technical documentation, tutorials, and guides. Help make our platform more accessible to developers worldwide.",
    icon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        className="w-6 h-6"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
        />
      </svg>
    ),
    benefits: [
      "Improve technical writing skills",
      "Shape developer experience",
      "Community recognition",
      "Documentation expertise",
    ],
  },
];

export default function GetInvolvedPage() {
  const [isWaitlistOpen, setIsWaitlistOpen] = useState(false);

  return (
    <div className="relative">
      {/* Hero section */}
      <div className="relative py-16 sm:py-24 bg-gradient-hero from-background-dark via-background-dark/95 to-background-dark/90 text-white">
        <Container>
          <div className="mx-auto max-w-2xl text-center">
            <Text as="h1" variant="display" className="mb-6">
              Get Involved
            </Text>
            <Text variant="body-lg" className="mb-8 text-neutral-200">
              Join our community of researchers, developers, and AI enthusiasts.
              Together, we're building the future of distributed AI development.
            </Text>
            <div className="flex flex-wrap justify-center gap-4">
              <Button
                size="lg"
                className="bg-gradient-primary hover:opacity-90"
                onClick={() => setIsWaitlistOpen(true)}
              >
                Join Waitlist
              </Button>
              <Link
                href="https://github.com/hopeatina/neuromosaic"
                className="inline-block"
              >
                <Button
                  variant="secondary"
                  size="lg"
                  className="bg-white/10 hover:bg-white/20 text-white border-none"
                >
                  View on GitHub
                </Button>
              </Link>
            </div>
          </div>
        </Container>
      </div>

      {/* Contribution areas */}
      <Container className="py-16">
        <Text as="h2" variant="h1" className="mb-6 text-center">
          Ways to Contribute
        </Text>
        <Text
          variant="body-lg"
          textColor="muted"
          className="mb-12 text-center max-w-2xl mx-auto"
        >
          Choose your path and start contributing to areas that match your
          interests and expertise.
        </Text>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          {contributionAreas.map((area) => (
            <Card
              key={area.title}
              className="p-8 flex flex-col h-full bg-white hover:shadow-lg transition-shadow duration-200"
            >
              <div className="mb-4 text-primary">{area.icon}</div>
              <Text as="h3" variant="h3" className="mb-3">
                {area.title}
              </Text>
              <Text textColor="muted" className="mb-6">
                {area.description}
              </Text>
              <div className="mt-auto">
                <Text
                  variant="small"
                  className="font-semibold text-primary mb-3"
                >
                  Benefits
                </Text>
                <ul className="space-y-2">
                  {area.benefits.map((benefit) => (
                    <li key={benefit} className="flex items-start gap-2">
                      <span className="block w-1.5 h-1.5 mt-2 rounded-full bg-secondary shrink-0" />
                      <Text variant="small" textColor="muted">
                        {benefit}
                      </Text>
                    </li>
                  ))}
                </ul>
              </div>
            </Card>
          ))}
        </div>
      </Container>

      <Modal
        isOpen={isWaitlistOpen}
        onOpenChange={setIsWaitlistOpen}
        size="wide"
      >
        <WaitlistForm onSuccess={() => setIsWaitlistOpen(false)} />
      </Modal>
    </div>
  );
}
