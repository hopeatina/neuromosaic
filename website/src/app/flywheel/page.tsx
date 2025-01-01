"use client";

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
      {/*-----------------------------------------
        Background decorative petals
      -----------------------------------------*/}
      <div className="absolute inset-0 -z-5 overflow-hidden">
        <FloatingPetal
          size="xl"
          className="absolute -top-44 -left-32"
          gradientId="petal-1"
        />
        <FloatingPetal
          size="lg"
          className="absolute -top-20 -right-16"
          gradientId="petal-2"
          delay={1}
        />
        <FloatingPetal
          size="md"
          className="absolute bottom-32 left-16"
          gradientId="petal-3"
          delay={2}
        />
        <FloatingPetal
          size="sm"
          className="absolute bottom-16 -right-8"
          gradientId="petal-4"
          delay={1.5}
        />
      </div>

      {/*-----------------------------------------
        Hero section
      -----------------------------------------*/}
      <div className="relative min-h-[40vh] flex items-center justify-center py-8 sm:py-12 z-10">
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

      {/*-----------------------------------------
        Flywheel steps around ring
      -----------------------------------------*/}
      <Container className="py-8 relative z-10">
        <FlywheelRing steps={flywheelSteps} ringSize={600} />
        {/* Mobile layout */}
        <div className="md:hidden space-y-8">
          {flywheelSteps.map((step, index) => (
            <Card
              key={step.title}
              className="p-6 bg-white/80 backdrop-blur-md shadow-md hover:shadow-lg transition-shadow duration-200"
            >
              <StepCardContent step={step} index={index} />
            </Card>
          ))}
        </div>
      </Container>

      {/*-----------------------------------------
        Benefits section
      -----------------------------------------*/}
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

/**
 * A small dedicated ring component that positions 5 steps in a circle + center.
 * For small screens, we fallback to a basic vertical layout.
 */
function FlywheelRing({
  steps,
  ringSize,
}: {
  steps: {
    title: string;
    description: string;
    details: string[];
  }[];
  ringSize: number;
}) {
  // We want 5 positions: top, right, bottom, left, center
  // Let's define them as percentages or pixel offsets
  // from the ring's center. ringSize=600 => radius=300
  // We'll place them so each card is well spaced.
  const radius = ringSize / 2;

  // Example positions (x,y) from ring center:
  // top => (0, -radius)
  // right => (radius, 0)
  // bottom => (0, radius)
  // left => (-radius, 0)
  // center => (0,0)

  const positions = [
    { x: 0, y: -radius }, // top
    { x: radius, y: 0 }, // right
    { x: 0, y: radius }, // bottom
    { x: -radius, y: 0 }, // left
    { x: 0, y: 0 }, // center
  ];

  return (
    <div
      className="
        relative mx-auto hidden md:block
        w-[600px] h-[600px]
      "
    >
      {/* The dashed ring */}
      <div
        className="
          absolute 
          w-full 
          h-full 
          border-4 border-dashed 
          border-primary/20 
          rounded-full
        "
      />

      {/* Place each step absolutely */}
      {steps.map((step, i) => {
        const p = positions[i] || { x: 0, y: 0 }; // fallback if >5
        return (
          <Card
            key={step.title}
            className="
              absolute p-6 bg-white/80 
              backdrop-blur-md shadow-md hover:shadow-lg 
              transition-shadow duration-200
              w-[220px] 
            "
            style={{
              // center the card at the ring center + offset
              left: `${ringSize / 2 + p.x - 110}px`, // half card width ~110
              top: `${ringSize / 2 + p.y - 60}px`, // half card height ~60
            }}
          >
            <StepCardContent step={step} index={i} />
          </Card>
        );
      })}
    </div>
  );
}

/**
 * On mobile screens, we fallback to a simple stacked layout:
 */
function StepCardContent({
  step,
  index,
}: {
  step: {
    title: string;
    description: string;
    details: string[];
  };
  index: number;
}) {
  return (
    <div>
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
    </div>
  );
}
