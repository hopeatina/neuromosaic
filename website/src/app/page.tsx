"use client";

import { useState } from "react";
import { Hero } from "@/components/sections/Hero";
import { QuickIntro } from "@/components/sections/QuickIntro";
import { Modal } from "@/components/ui/Modal";
import { WaitlistForm } from "@/components/forms/WaitlistForm";

export default function HomePage() {
  const [isWaitlistOpen, setIsWaitlistOpen] = useState(false);

  const modalContent = (
    <WaitlistForm onSuccess={() => setIsWaitlistOpen(false)} />
  );

  return (
    <>
      <Hero onWaitlistClick={() => setIsWaitlistOpen(true)} />
      <QuickIntro />
      <Modal
        isOpen={isWaitlistOpen}
        onOpenChange={setIsWaitlistOpen}
        title="Join the Waitlist"
        description="Sign up to be among the first to access our platform when we launch."
        children={modalContent}
      />
    </>
  );
}
