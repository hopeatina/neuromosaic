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
import React from "react";

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
      {React.createElement(Modal, {
        isOpen: isWaitlistOpen,
        onOpenChange: setIsWaitlistOpen,
        title: "Join the Waitlist",
        description:
          "Sign up to be among the first to access our platform when we launch.",
        children: <WaitlistForm onSuccess={() => setIsWaitlistOpen(false)} />,
      })}
    </>
  );
}
