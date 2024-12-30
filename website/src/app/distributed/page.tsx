import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

const features = [
  {
    title: "Resource Management",
    description:
      "Intelligent allocation and management of computing resources across the distributed network.",
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
      "Efficient distribution of training tasks and workloads across available computing nodes.",
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
      "Real-time monitoring and visualization of training progress across the distributed network.",
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
    <div className="relative">
      {/* Hero section */}
      <div className="relative py-16 sm:py-24">
        <Container>
          <div className="mx-auto max-w-2xl text-center">
            <Text as="h1" variant="display" className="mb-6">
              Distributed Platform
            </Text>
            <Text variant="body-lg" textColor="muted" className="mb-8">
              Access powerful distributed computing resources for AI model
              training and experimentation. Join our network of contributors to
              accelerate development.
            </Text>
            <div className="flex flex-wrap justify-center gap-4">
              <Link href="/get-involved#join-waitlist" className="inline-block">
                <Button size="lg">Request Access</Button>
              </Link>
              <Link href="/docs" className="inline-block">
                <Button variant="secondary" size="lg">
                  View Documentation
                </Button>
              </Link>
            </div>
          </div>
        </Container>
      </div>

      {/* Features */}
      <Container className="py-16">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {features.map((feature) => (
            <Card key={feature.title} className="p-6">
              <div className="mb-4 text-primary">{feature.icon}</div>
              <Text as="h3" variant="h3" className="mb-3">
                {feature.title}
              </Text>
              <Text textColor="muted">{feature.description}</Text>
            </Card>
          ))}
        </div>
      </Container>

      {/* How it works */}
      <div className="bg-neutral-50 border-y border-neutral-200">
        <Container className="py-16">
          <div className="mx-auto max-w-3xl">
            <Text as="h2" variant="h1" className="mb-12 text-center">
              How It Works
            </Text>
            <div className="space-y-12">
              <div>
                <Text as="h3" variant="h2" className="mb-4">
                  1. Join the Network
                </Text>
                <Text textColor="muted">
                  Sign up and connect your computing resources to our
                  distributed network. Our platform automatically manages
                  resource allocation and task distribution.
                </Text>
              </div>
              <div>
                <Text as="h3" variant="h2" className="mb-4">
                  2. Configure Resources
                </Text>
                <Text textColor="muted">
                  Specify the amount of computing power you want to contribute
                  and set your availability preferences. Our system ensures
                  optimal resource utilization.
                </Text>
              </div>
              <div>
                <Text as="h3" variant="h2" className="mb-4">
                  3. Start Contributing
                </Text>
                <Text textColor="muted">
                  Begin participating in distributed training tasks. Monitor
                  your contribution metrics and earn rewards for your
                  participation in the network.
                </Text>
              </div>
            </div>
          </div>
        </Container>
      </div>

      {/* CTA section */}
      <Container className="py-16">
        <Card className="p-8 text-center">
          <Text as="h2" variant="h2" className="mb-4">
            Ready to Join?
          </Text>
          <Text textColor="muted" className="mb-8 max-w-2xl mx-auto">
            Be part of our distributed computing network and help accelerate AI
            development. Early contributors get priority access and additional
            benefits.
          </Text>
          <Button size="lg" asChild>
            <Link href="/get-involved#join-waitlist">Request Early Access</Link>
          </Button>
        </Card>
      </Container>
    </div>
  );
}
