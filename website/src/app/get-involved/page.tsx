import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

const contributionAreas = [
  {
    title: "Model Development",
    description:
      "Contribute to model architecture improvements, training optimizations, and new capability development.",
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
  },
  {
    title: "Infrastructure",
    description:
      "Help build and maintain the distributed computing infrastructure that powers our platform.",
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
  },
  {
    title: "Documentation",
    description:
      "Write and improve documentation to help others understand and use the platform effectively.",
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
  },
];

export default function GetInvolvedPage() {
  return (
    <div className="relative">
      {/* Hero section */}
      <div className="relative py-16 sm:py-24">
        <Container>
          <div className="mx-auto max-w-2xl text-center">
            <Text as="h1" variant="display" className="mb-6">
              Get Involved
            </Text>
            <Text variant="body-lg" textColor="muted" className="mb-8">
              Join our community of researchers, developers, and AI enthusiasts
              working together to advance the field of machine learning.
            </Text>
            <div className="flex flex-wrap justify-center gap-4">
              <Link href="#join-waitlist" className="inline-block">
                <Button size="lg">Join Waitlist</Button>
              </Link>
              <Link
                href="https://github.com/neuromosaic"
                className="inline-block"
              >
                <Button variant="secondary" size="lg">
                  View on GitHub
                </Button>
              </Link>
            </div>
          </div>
        </Container>
      </div>

      {/* Contribution areas */}
      <Container className="py-16">
        <Text as="h2" variant="h1" className="mb-12 text-center">
          Ways to Contribute
        </Text>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          {contributionAreas.map((area) => (
            <Card key={area.title} className="p-6">
              <div className="mb-4 text-primary">{area.icon}</div>
              <Text as="h3" variant="h3" className="mb-3">
                {area.title}
              </Text>
              <Text textColor="muted">{area.description}</Text>
            </Card>
          ))}
        </div>
      </Container>

      {/* Waitlist section */}
      <div className="bg-neutral-50 border-y border-neutral-200">
        <Container className="py-16">
          <div className="mx-auto max-w-2xl">
            <Card className="p-8" id="join-waitlist">
              <Text as="h2" variant="h2" className="mb-6">
                Join the Waitlist
              </Text>
              <Text textColor="muted" className="mb-8">
                Sign up to be among the first to access our platform when we
                launch. Early contributors will have the opportunity to shape
                the future of distributed AI development.
              </Text>
              <form className="space-y-4">
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-neutral-700 mb-1"
                  >
                    Email address
                  </label>
                  <input
                    type="email"
                    name="email"
                    id="email"
                    className="form-input"
                    placeholder="you@example.com"
                  />
                </div>
                <div>
                  <label
                    htmlFor="interests"
                    className="block text-sm font-medium text-neutral-700 mb-1"
                  >
                    Areas of interest
                  </label>
                  <select
                    id="interests"
                    name="interests"
                    className="form-input"
                    defaultValue=""
                  >
                    <option value="" disabled>
                      Select an area
                    </option>
                    <option value="model-development">Model Development</option>
                    <option value="infrastructure">Infrastructure</option>
                    <option value="documentation">Documentation</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <Button type="submit" className="w-full">
                  Join Waitlist
                </Button>
              </form>
            </Card>
          </div>
        </Container>
      </div>
    </div>
  );
}
