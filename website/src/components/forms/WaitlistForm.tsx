"use client";

import { useEffect, useRef } from "react";

interface WaitlistFormProps {
  onSuccess?: () => void;
}

export function WaitlistForm({ onSuccess }: WaitlistFormProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    // Add a message listener to handle successful subscriptions
    const handleMessage = (event: MessageEvent) => {
      if (
        event.origin === "https://neuromosaic.substack.com" &&
        event.data?.type === "subscribe" &&
        event.data?.successful
      ) {
        onSuccess?.();
      }
    };

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, [onSuccess]);

  return (
    <iframe
      ref={iframeRef}
      src="https://neuromosaic.substack.com/embed"
      width="480"
      height="320"
      style={{
        border: "1px solid #EEE",
        background: "white",
      }}
      frameBorder="0"
      scrolling="no"
    />
  );
}
