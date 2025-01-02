import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import Link from "next/link";

const updates = [
  {
    date: "2024 Q1",
    title: "Distributed Training Beta",
    description:
      "Launch of our distributed training infrastructure beta program, enabling parallel model training across multiple nodes.",
    type: "feature",
    link: "/distributed",
  },
  {
    date: "2024 Q1",
    title: "Community Contributions",
    description:
      "New contribution guidelines and documentation for community members looking to participate in development.",
    type: "community",
    link: "/docs/contributing",
  },
  {
    date: "2024 Q1",
    title: "Platform Architecture",
    description:
      "Major updates to our core platform architecture, improving scalability and resource utilization.",
    type: "technical",
    link: "/docs/architecture",
  },
];

const roadmap = [
  {
    quarter: "Q2 2024",
    items: [
      "Enhanced monitoring and analytics dashboard",
      "Improved resource allocation algorithms",
      "Extended API documentation",
    ],
  },
  {
    quarter: "Q3 2024",
    items: [
      "Advanced model versioning system",
      "Automated performance optimization",
      "Community contribution rewards",
    ],
  },
];

export default function UpdatesPage() {
  return (
    <div className="relative">
      {/* Hero section */}
      <div className="relative py-16 sm:py-24">
        <Container>
          <div className="mx-auto max-w-2xl text-center">
            <Text as="h1" variant="display" className="mb-6">
              Platform Updates
            </Text>
            <Text variant="body-lg" textColor="muted" className="mb-8">
              Stay informed about the latest developments, features, and
              improvements to the Neuromosaic platform.
            </Text>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                href="https://neuromosaic.mintlify.app/"
                className="inline-block"
              >
                <Button size="lg">View Documentation</Button>
              </Link>
              <Link
                href="https://github.com/hopeatina/neuromosaic"
                className="inline-block"
              >
                <Button variant="secondary" size="lg">
                  GitHub Releases
                </Button>
              </Link>
            </div>
          </div>
        </Container>
      </div>

      {/* Recent Updates */}
      <Container className="py-16">
        <Text as="h2" variant="h1" className="mb-12">
          Recent Updates
        </Text>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          {updates.map((update) => (
            <Link href={update.link} key={update.title}>
              <Card className="p-6 h-full hover:shadow-lg transition-shadow duration-200">
                <div className="flex justify-between items-start mb-4">
                  <span className="inline-flex items-center rounded-md bg-primary/10 px-2 py-1 text-sm font-medium text-primary">
                    {update.type}
                  </span>
                  <Text variant="small" textColor="muted">
                    {update.date}
                  </Text>
                </div>
                <Text as="h3" variant="h3" className="mb-3">
                  {update.title}
                </Text>
                <Text textColor="muted">{update.description}</Text>
              </Card>
            </Link>
          ))}
        </div>
      </Container>

      {/* Roadmap section */}
      <div className="bg-neutral-50 border-y border-neutral-200">
        <Container className="py-16">
          <Text as="h2" variant="h1" className="mb-12">
            Development Roadmap
          </Text>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
            {roadmap.map((quarter) => (
              <Card key={quarter.quarter} className="p-6">
                <Text as="h3" variant="h3" className="mb-6">
                  {quarter.quarter}
                </Text>
                <ul className="space-y-4">
                  {quarter.items.map((item) => (
                    <li key={item} className="flex items-start gap-3">
                      <span className="block w-2 h-2 mt-2 rounded-full bg-primary shrink-0" />
                      <Text textColor="muted">{item}</Text>
                    </li>
                  ))}
                </ul>
              </Card>
            ))}
          </div>
        </Container>
      </div>
    </div>
  );
}
