import { Container } from "@/components/ui/Container";
import { Text } from "@/components/ui/Text";
import { Card } from "@/components/ui/Card";
import { FloatingPetal } from "@/components/ui/FloatingPetal";

const flywheelSteps = [
  {
    title: "Model Training",
    description:
      "Initial model training using distributed computing resources and high-quality datasets.",
    details: [
      "Parallel training across nodes",
      "Resource optimization",
      "Progress monitoring",
      "Performance metrics tracking",
    ],
  },
  {
    title: "Result Analysis",
    description:
      "Comprehensive analysis of model performance, identifying strengths and areas for improvement.",
    details: [
      "Performance evaluation",
      "Error analysis",
      "Behavior patterns",
      "Edge case identification",
    ],
  },
  {
    title: "Capability Enhancement",
    description:
      "Systematic improvement of model capabilities based on analysis results and community feedback.",
    details: [
      "Architecture refinement",
      "Parameter optimization",
      "Feature engineering",
      "Training strategy updates",
    ],
  },
  {
    title: "Example Generation",
    description:
      "Creation of new training examples focusing on identified improvement areas.",
    details: [
      "Data augmentation",
      "Synthetic data generation",
      "Edge case coverage",
      "Quality validation",
    ],
  },
  {
    title: "Data Integration",
    description:
      "Integration of new data into the training pipeline, ensuring quality and consistency.",
    details: [
      "Data preprocessing",
      "Quality assurance",
      "Pipeline optimization",
      "Version control",
    ],
  },
];

export default function FlywheelPage() {
  return (
    <div className="relative overflow-hidden">
      {/* Background decorative petals */}
      <div className="absolute inset-0 -z-5 overflow-hidden">
        {/* Large petal top left */}
        <FloatingPetal
          size="xl"
          className="absolute -top-44 -left-32"
          gradientId="petal-1"
        />

        {/* Medium petal top right */}
        <FloatingPetal
          size="lg"
          className="absolute -top-20 -right-16"
          gradientId="petal-2"
          delay={1}
        />

        {/* Small petal bottom left */}
        <FloatingPetal
          size="md"
          className="absolute bottom-32 left-16"
          gradientId="petal-3"
          delay={2}
        />

        {/* Extra small petal bottom right */}
        <FloatingPetal
          size="sm"
          className="absolute bottom-16 -right-8"
          gradientId="petal-4"
          delay={1.5}
        />
      </div>

      {/* Hero section */}
      <div className="relative min-h-[60vh] flex items-center justify-center py-16 sm:py-24 z-10">
        <Container>
          <div className="mx-auto max-w-3xl text-center flex flex-col items-center justify-center">
            <Text as="h1" variant="display" className="mb-6 text-gradient">
              The Neuromosaic Flywheel
            </Text>
            <Text
              variant="body-lg"
              textColor="muted"
              className="mb-8 max-w-2xl"
            >
              Our iterative approach to model improvement combines distributed
              computing with systematic refinement, creating a self-reinforcing
              cycle of continuous enhancement.
            </Text>
          </div>
        </Container>
      </div>

      {/* Flywheel steps */}
      <Container className="py-16 relative z-10">
        <div className="relative">
          {/* Curved dashed ring behind cards */}
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="w-[600px] h-[600px] border-4 border-dashed border-primary/20 rounded-full" />
          </div>

          {/* Steps */}
          <div className="relative grid grid-cols-1 gap-12 md:grid-cols-2 lg:grid-cols-3">
            {flywheelSteps.map((step, index) => (
              <Card
                key={step.title}
                className="relative p-6 bg-white/80 backdrop-blur-md shadow-md hover:shadow-lg transition-shadow duration-200"
              >
                <div className="mb-4">
                  <Text
                    as="span"
                    variant="small"
                    textColor="primary"
                    className="uppercase font-semibold tracking-wide"
                  >
                    Step {index + 1}
                  </Text>
                </div>
                <Text as="h3" variant="h3" className="mb-3">
                  {step.title}
                </Text>
                <Text textColor="muted" className="mb-6">
                  {step.description}
                </Text>
                <ul className="space-y-2">
                  {step.details.map((detail) => (
                    <li
                      key={detail}
                      className="flex items-start gap-2 text-sm text-neutral-700 leading-relaxed"
                    >
                      <span className="block w-2 h-2 mt-[6px] rounded-full bg-primary shrink-0" />
                      {detail}
                    </li>
                  ))}
                </ul>
              </Card>
            ))}
          </div>
        </div>
      </Container>

      {/* Benefits section */}
      <Container className="py-16 relative z-10">
        <div className="mx-auto max-w-3xl text-center mb-12">
          <Text as="h2" variant="h1" className="mb-6">
            Benefits of the Flywheel
          </Text>
          <Text variant="body-lg" textColor="muted">
            The flywheel effect creates a virtuous cycle where each improvement
            builds upon previous successes, leading to exponential gains in
            model performance and capabilities.
          </Text>
        </div>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
          <Card className="p-6 text-left bg-white/80 backdrop-blur-md shadow-sm hover:shadow-md transition-shadow duration-200">
            <Text as="h3" variant="h3" className="mb-3">
              Continuous Improvement
            </Text>
            <Text textColor="muted">
              Each iteration of the flywheel brings incremental improvements,
              building momentum for more significant advances over time.
            </Text>
          </Card>
          <Card className="p-6 text-left bg-white/80 backdrop-blur-md shadow-sm hover:shadow-md transition-shadow duration-200">
            <Text as="h3" variant="h3" className="mb-3">
              Community Synergy
            </Text>
            <Text textColor="muted">
              The collaborative nature of the platform allows the community to
              contribute their expertise at every stage of the process.
            </Text>
          </Card>
        </div>
      </Container>
    </div>
  );
}
