"use client";

import { useState } from "react";
import { Hero } from "@/components/sections/Hero";
import { WhatIsNeuromosaic } from "@/components/sections/WhatIsNeuromosaic";
import { WhyNeuromosaic } from "@/components/sections/WhyNeuromosaic";
import { HowItWorks } from "@/components/sections/HowItWorks";
import { UseCases } from "@/components/sections/UseCases";
import { FAQs } from "@/components/sections/FAQs";
import { Modal } from "@/components/ui/Modal";
import { WaitlistForm } from "@/components/forms/WaitlistForm";
import { FloatingPetal } from "@/components/ui/FloatingPetal";

export default function HomePage() {
  const [isWaitlistOpen, setIsWaitlistOpen] = useState(false);

  return (
    <div className="relative">
      {/* Hero */}
      <div className="relative">
        <Hero onWaitlistClick={() => setIsWaitlistOpen(true)} />
      </div>

      {/* WhatIs - primary-ultralight */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-b from-primary-ultralight to-primary-ultralight" />
        <div className="relative">
          <FloatingPetal
            className="absolute right-[10%] top-[15%]"
            size="xl"
            delay={1}
            gradientId="petal1"
            randomness={false}
          />
          <FloatingPetal
            className="absolute left-[5%] bottom-[20%]"
            size="lg"
            delay={3}
            gradientId="petal2"
          />
          <WhatIsNeuromosaic />
        </div>
      </div>

      {/* Why - secondary-ultralight */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-b from-primary-ultralight via-[#f1f0ff] to-secondary-ultralight" />
        <div className="relative">
          <FloatingPetal
            className="absolute left-[15%] top-[25%]"
            size="xl"
            delay={2}
            gradientId="petal3"
          />
          <FloatingPetal
            className="absolute right-[8%] bottom-[15%]"
            size="lg"
            delay={4}
            gradientId="petal4"
          />
          <WhyNeuromosaic />
        </div>
      </div>

      {/* HowItWorks - accent-ultralight */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-b from-secondary-ultralight via-[#f7f1ff] to-accent-ultralight" />
        <div className="relative">
          <FloatingPetal
            className="absolute right-[12%] top-[10%]"
            size="xl"
            delay={0}
            gradientId="petal5"
          />
          <FloatingPetal
            className="absolute left-[10%] bottom-[25%]"
            size="lg"
            delay={2}
            gradientId="petal6"
          />
          <HowItWorks />
        </div>
      </div>

      {/* UseCases - primary-faded */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-b from-accent-ultralight via-[#f9f2ff] to-primary-faded" />
        <div className="relative">
          <FloatingPetal
            className="absolute right-[15%] top-[20%]"
            size="xl"
            delay={1}
            gradientId="petal7"
          />
          <FloatingPetal
            className="absolute left-[8%] bottom-[15%]"
            size="lg"
            delay={3}
            gradientId="petal8"
          />
          <UseCases />
        </div>
      </div>

      {/* FAQs - secondary-faded */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-b from-primary-faded via-[#f6f4ff] to-secondary-faded" />
        <div className="relative">
          <FloatingPetal
            className="absolute left-[12%] top-[10%]"
            size="xl"
            delay={2}
            gradientId="petal9"
          />
          <FloatingPetal
            className="absolute right-[10%] bottom-[20%]"
            size="lg"
            delay={4}
            gradientId="petal10"
          />
          <FAQs />
        </div>
      </div>

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
