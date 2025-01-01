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

export default function HomePage() {
  const [isWaitlistOpen, setIsWaitlistOpen] = useState(false);

  return (
    <>
      <Hero onWaitlistClick={() => setIsWaitlistOpen(true)} />
      <WhatIsNeuromosaic />
      <WhyNeuromosaic />
      <HowItWorks />
      <UseCases />
      <FAQs />
      <Modal
        isOpen={isWaitlistOpen}
        onOpenChange={setIsWaitlistOpen}
        size="wide"
      >
        <WaitlistForm onSuccess={() => setIsWaitlistOpen(false)} />
      </Modal>
    </>
  );
}
