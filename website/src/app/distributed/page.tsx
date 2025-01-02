import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { FloatingPetal } from "@/components/ui/FloatingPetal";

const features = [
  {
    title: "Resource Management",
    description:
      "Intelligent allocation and optimization of computing resources across the distributed network.",
    details: [
      "Dynamic resource scaling",
      "Load balancing",
      "Performance monitoring",
      "Cost optimization",
    ],
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
          d="M21 7.5l-2.25-1.313M21 7.5v2.25m0-2.25l-2.25 1.313M3 7.5l2.25-1.313M3 7.5l2.25 1.313M3 7.5v2.25m9 3l2.25-1.313M12 12.75l-2.25-1.313M12 12.75V15m0 6.75l2.25-1.313M12 21.75V19.5m0 2.25l-2.25-1.313m0-16.875L12 2.25l2.25 1.313M21 14.25v2.25l-2.25 1.313m-13.5 0L3 16.5v-2.25"
        />
      </svg>
    ),
  },
  {
    title: "Task Distribution",
    description:
      "Advanced workload distribution system that ensures optimal training performance across nodes.",
    details: [
      "Smart task allocation",
      "Priority scheduling",
      "Failure recovery",
      "Progress tracking",
    ],
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
          d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5"
        />
      </svg>
    ),
  },
  {
    title: "Progress Tracking",
    description:
      "Real-time monitoring and visualization of training progress with detailed analytics.",
    details: [
      "Performance metrics",
      "Resource utilization",
      "Training insights",
      "Error analysis",
    ],
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
          d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"
        />
      </svg>
    ),
  },
];

export default function DistributedPage() {
  return (
    <div className="relative overflow-hidden">
      {/* Background petals */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <FloatingPetal
          size="xl"
          className="absolute -top-44 -right-32"
          gradientId="petal-1"
        />
        <FloatingPetal
          size="lg"
          className="absolute top-96 -left-16"
          gradientId="petal-2"
          delay={1}
        />
        <FloatingPetal
          size="md"
          className="absolute bottom-32 right-16"
          gradientId="petal-3"
          delay={2}
        />
      </div>

      {/* Hero section */}
      <div className="relative py-16 sm:py-24 bg-gradient-hero from-background-dark via-background-dark/95 to-background-dark/90">
        <Container>
          <div className="mx-auto max-w-2xl text-center">
            <Text
              as="h1"
              variant="display"
              className="mb-6 text-white text-center"
            >
              Distributed Platform
            </Text>
            <Text
              variant="body-lg"
              className="mb-8 text-neutral-200 text-center"
            >
              Harness the power of distributed computing for AI model training
              and experimentation. Our platform enables efficient resource
              utilization and seamless collaboration across nodes.
            </Text>
            <div className="flex flex-wrap justify-center gap-4">
              <Link href="/get-involved#join-waitlist" className="inline-block">
                <Button
                  size="lg"
                  className="bg-gradient-primary hover:opacity-90"
                >
                  Request Access
                </Button>
              </Link>
              <Link
                href="https://neuromosaic.mintlify.app/"
                className="inline-block"
              >
                <Button
                  variant="secondary"
                  size="lg"
                  className="bg-white/10 hover:bg-white/20 text-white border-none"
                >
                  View Documentation
                </Button>
              </Link>
            </div>
          </div>
        </Container>
      </div>

      {/* Features */}
      <Container className="py-16">
        <div className="text-center mb-12">
          <Text as="h2" variant="h1" className="mb-6 text-center">
            Platform Features
          </Text>
          <Text
            variant="body-lg"
            textColor="muted"
            className="mb-12 text-center max-w-2xl mx-auto"
          >
            Our distributed platform is built for performance, scalability, and
            ease of use.
          </Text>
        </div>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {features.map((feature) => (
            <Card
              key={feature.title}
              className="p-8 bg-white hover:shadow-lg transition-shadow duration-200"
            >
              <div className="mb-4 text-primary">{feature.icon}</div>
              <Text as="h3" variant="h3" className="mb-3">
                {feature.title}
              </Text>
              <Text textColor="muted" className="mb-6 text-neutral-700">
                {feature.description}
              </Text>
              <ul className="space-y-2">
                {feature.details.map((detail) => (
                  <li key={detail} className="flex items-start gap-2">
                    <span className="block w-1.5 h-1.5 mt-2 rounded-full bg-secondary shrink-0" />
                    <Text variant="small" className="text-neutral-600">
                      {detail}
                    </Text>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </div>
      </Container>

      {/* How it works */}
      <div className="bg-gradient-dark border-y border-white/10">
        <Container className="py-16">
          <div className="mx-auto max-w-3xl">
            <Text as="h2" variant="h1" className="mb-12 text-center text-white">
              How It Works
            </Text>
            <div className="space-y-12">
              <div className="relative pl-8 pb-12 border-l-2 border-primary/20 last:border-0">
                <div className="absolute left-0 -translate-x-1/2 w-4 h-4 rounded-full bg-primary" />
                <Text as="h3" variant="h2" className="mb-4 text-white">
                  1. Join the Network
                </Text>
                <Text className="text-neutral-300">
                  Connect your computing resources to our distributed network.
                  Our platform automatically handles resource allocation and
                  task distribution, ensuring optimal utilization of your
                  hardware.
                </Text>
              </div>
              <div className="relative pl-8 pb-12 border-l-2 border-primary/20 last:border-0">
                <div className="absolute left-0 -translate-x-1/2 w-4 h-4 rounded-full bg-primary" />
                <Text as="h3" variant="h2" className="mb-4 text-white">
                  2. Configure Resources
                </Text>
                <Text className="text-neutral-300">
                  Set your resource availability preferences and constraints.
                  Our intelligent system ensures your hardware is utilized
                  according to your specifications while maintaining optimal
                  network performance.
                </Text>
              </div>
              <div className="relative pl-8">
                <div className="absolute left-0 -translate-x-1/2 w-4 h-4 rounded-full bg-primary" />
                <Text as="h3" variant="h2" className="mb-4 text-white">
                  3. Start Contributing
                </Text>
                <Text className="text-neutral-300">
                  Begin participating in distributed training tasks. Monitor
                  your contribution metrics in real-time and earn rewards based
                  on your participation and resource provision.
                </Text>
              </div>
            </div>
          </div>
        </Container>
      </div>

      {/* CTA section */}
      <Container className="py-16">
        <Card className="p-8 text-center bg-gradient-primary text-white">
          <Text as="h2" variant="h2" className="mb-4 text-center">
            Ready to Join?
          </Text>
          <Text className="mb-8 max-w-2xl mx-auto text-center text-white/90">
            Be part of our distributed computing network and help accelerate AI
            development. Early contributors receive priority access and
            additional benefits.
          </Text>
          <Link href="/get-involved#join-waitlist">
            <Button
              size="lg"
              className="bg-white text-primary hover:bg-white/90"
            >
              Request Early Access
            </Button>
          </Link>
        </Card>
      </Container>
    </div>
  );
}
