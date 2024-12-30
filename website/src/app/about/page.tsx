import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";

const architecturePoints = [
  {
    title: "Distributed Training",
    description:
      "Our platform distributes model training across multiple nodes, enabling faster iteration and more comprehensive testing.",
  },
  {
    title: "Data Pipeline",
    description:
      "Efficient data processing and augmentation pipelines ensure high-quality training data for model improvement.",
  },
  {
    title: "Model Versioning",
    description:
      "Sophisticated version control for models, allowing easy tracking of improvements and rollbacks when needed.",
  },
  {
    title: "Result Analysis",
    description:
      "Comprehensive analytics and visualization tools to understand model performance and identify areas for improvement.",
  },
];

export default function AboutPage() {
  return (
    <div className="relative">
      {/* Hero section */}
      <div className="relative py-16 sm:py-24">
        <Container>
          <div className="mx-auto max-w-2xl lg:text-center">
            <Text as="h1" variant="display" className="mb-6">
              About Neuromosaic
            </Text>
            <Text variant="body-lg" textColor="muted" className="mb-8">
              Neuromosaic is an open-source platform that enables distributed AI
              model training and refinement through community collaboration. Our
              goal is to accelerate AI development by combining distributed
              computing with collective expertise.
            </Text>
          </div>
        </Container>
      </div>

      {/* Mission section */}
      <Container className="py-16">
        <div className="grid grid-cols-1 gap-16 lg:grid-cols-2">
          <div>
            <Text as="h2" variant="h1" className="mb-6">
              Our Mission
            </Text>
            <Text variant="body-lg" textColor="muted" className="mb-8">
              We believe that the future of AI development lies in collaborative
              efforts and distributed computing. By providing tools and
              infrastructure for the community to work together, we can
              accelerate the pace of innovation while ensuring transparency and
              ethical development.
            </Text>
            <div className="space-y-4">
              <Text variant="body" textColor="muted">
                Key objectives:
              </Text>
              <ul className="list-disc list-inside space-y-2 text-neutral-700">
                <li>Enable distributed model training and experimentation</li>
                <li>Foster collaboration among researchers and developers</li>
                <li>Maintain transparency in AI development</li>
                <li>Accelerate the pace of AI innovation</li>
              </ul>
            </div>
          </div>
          <div>
            <Text as="h2" variant="h1" className="mb-6">
              Why Distributed?
            </Text>
            <Text variant="body-lg" textColor="muted" className="mb-8">
              Distributed computing allows us to harness the collective power of
              many systems, leading to faster training times and more
              comprehensive testing. This approach also enables:
            </Text>
            <div className="space-y-4">
              <ul className="list-disc list-inside space-y-2 text-neutral-700">
                <li>Parallel experimentation across multiple nodes</li>
                <li>Efficient resource utilization</li>
                <li>Scalable infrastructure for growing demands</li>
                <li>Resilient and fault-tolerant operations</li>
              </ul>
            </div>
          </div>
        </div>
      </Container>

      {/* Architecture section */}
      <Container className="py-16">
        <Text as="h2" variant="h1" className="mb-12 text-center">
          Platform Architecture
        </Text>
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {architecturePoints.map((point) => (
            <Card key={point.title} className="p-6">
              <Text as="h3" variant="h3" className="mb-3">
                {point.title}
              </Text>
              <Text textColor="muted">{point.description}</Text>
            </Card>
          ))}
        </div>
      </Container>
    </div>
  );
}
